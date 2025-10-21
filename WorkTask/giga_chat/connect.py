
from gigachat import GigaChat
import sys

import json
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np


sys.stdout.reconfigure(encoding='utf-8')

api_key = '' 

def giga_chat():
   # Укажите ключ авторизации, полученный в личном кабинете, в интерфейсе проекта GigaChat API
   with GigaChat(credentials=api_key, verify_ssl_certs=False) as giga:
      response = giga.chat("сколько будет 2 + 2?")
      return response.choices[0].message.content

print(giga_chat())



def chunk_large_file(file_path, chunk_size=50, overlap=10):
    chunks = []
    current_chunk_words = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            for word in words:
                current_chunk_words.append(word)
                if len(current_chunk_words) >= chunk_size:
                    chunk_text = " ".join(current_chunk_words)
                    chunks.append(chunk_text)
                    # Сохраняем перекрытие
                    if overlap > 0:
                        current_chunk_words = current_chunk_words[-overlap:]
                    else:
                        current_chunk_words = []
    # Остаток
    if current_chunk_words:
        chunks.append(" ".join(current_chunk_words))
    return chunks

def create_and_store_embeddings(file_path, model_name='paraphrase-MiniLM-L6-v2', chunk_size=50, overlap=10, save_index=True):
    # 1. Загружаем модель
    model = SentenceTransformer(model_name)
#    print(f"Загружена модель: {model_name}")

    # 2. Создаем чанки из файла
    chunks = chunk_large_file(file_path, chunk_size, overlap)
#    print(f"Создано {len(chunks)} чанков")

    # 3. Вычисляем эмбеддинги
    embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype=np.float32)

    # 4. Создаем FAISS индекс
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # 5. Добавляем эмбеддинги
    index.add(embeddings)

    # 6. Сохраняем индекс И чанки
    if save_index:
        # Сохраняем FAISS индекс
        faiss.write_index(index, 'faiss_index.bin')
        
        # Сохраняем чанки в JSON файл
        with open('chunks_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        
#        print("Индекс сохранен в 'faiss_index.bin'.")
#        print("Чанки сохранены в 'chunks_metadata.json'.")

    return index, chunks

def load_chunks_metadata():
    """Загружает сохраненные чанки"""
    try:
        with open('chunks_metadata.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Ошибка: Файл chunks_metadata.json не найден!")
        return []

def user_question_embending(question: str, model_name='paraphrase-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embedding = model.encode(question, convert_to_numpy=True, show_progress_bar=False, normalize_embeddings=True)
    embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
    return embedding

def search_similar_chunks(question: str, index_path='faiss_index.bin', top_k=3, model_name='paraphrase-MiniLM-L6-v2'):
    # Загружаем индекс
    index = faiss.read_index(index_path)
    
    # Загружаем сохраненные чанки (а не создаем заново!)
    chunks = load_chunks_metadata()
    
    if not chunks:
        print("Ошибка: Не удалось загрузить чанки!")
        return []
    
    # Получаем эмбеддинг вопроса
    query_embedding = user_question_embending(question, model_name)
    
    # Поиск top_k похожих векторов
    distances, indices = index.search(query_embedding, top_k)
    
    # Собираем результаты
    results = []
    for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
        if idx < len(chunks):
            results.append({
                'chunk': chunks[idx],
                'distance': float(distance),
                'index': idx,
                'rank': i + 1
            })
        else:
            print(f"Предупреждение: индекс {idx} превышает количество чанков ({len(chunks)})")
    
    return results

# Пример использования:
if __name__ == "__main__":

    print("=== СОЗДАНИЕ ИНДЕКСА ===")
    create_and_store_embeddings('text.txt')
    
    print("\n=== ПОИСК ===")

    question = "Что такое философия стоиков?"
    results = search_similar_chunks(question, top_k=3)
    
    print(f"Результаты для запроса: '{question}'")
    print("=" * 60)
    
    for result in results:
        print(f"\n{result['rank']}. Расстояние: {result['distance']:.4f} (индекс: {result['index']})")
        print(f"Текст: {result['chunk']}")
        print("-" * 40)