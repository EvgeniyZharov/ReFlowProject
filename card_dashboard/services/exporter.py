import csv
import pandas as pd
import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database.connect_to_db import (get_all_cards, get_api_keys, get_wb_accounts, get_sync_logs, 
get_wb_cards_by_account, get_wb_sizes_by_card, get_wb_images_by_card)


def export_csv(**kwargs : any) -> str:
	with open('export.csv', 'w', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(['Карточки'])
		writer.writerow(['id', 'title', 'description', 'price'])
		for card in kwargs['cards']:
			writer.writerow([card.id, card.title, card.description, card.price])
        
   
	with open('export.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([''])
		writer.writerow(['API ключи'])
		writer.writerow(['id', 'title', 'api_key'])
		for api_key in kwargs['api_keys']:
			writer.writerow([api_key.id, api_key.title, api_key.api_key])

	with open('export.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([''])
		writer.writerow(['Аккаунты WB'])
		writer.writerow(['id', 'title', 'api_key', 'account_name', 'company_name', 'is_active', 'created_at', 'last_sync'])
		for wb_account in kwargs['wb_accounts']:
			writer.writerow([wb_account.id, wb_account.title, wb_account.api_key, wb_account.account_name, wb_account.company_name, wb_account.is_active, wb_account.created_at, wb_account.last_sync])

	with open('export.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([''])
		writer.writerow(['Логи синхронизации'])
		writer.writerow(['id', 'account_id', 'status', 'cards_processed', 'error_message', 'sync_date'])
		for sync_log in kwargs['sync_logs']:
			writer.writerow([sync_log.id, sync_log.account_id, sync_log.status, sync_log.cards_processed, sync_log.error_message, sync_log.sync_date])

	with open('export.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([''])
		writer.writerow(['Карточки WB'])
		writer.writerow(['id', 'account_id', 'nm_id', 'sku', 'imt_name', 'subject_name', 'brand_name', 'current_price', 'original_price', 'total_quantity', 'created_at', 'updated_at'])
		for wb_card in kwargs['wb_cards']:
			writer.writerow([wb_card.id, wb_card.account_id, wb_card.nm_id, wb_card.sku, wb_card.imt_name, wb_card.subject_name, wb_card.brand_name, wb_card.current_price, wb_card.original_price, wb_card.total_quantity, wb_card.created_at, wb_card.updated_at])

	with open('export.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([''])
		writer.writerow(['Размеры WB'])
		writer.writerow(['id', 'card_id', 'size_name', 'size_sku', 'quantity', 'barcode'])
		for wb_size in kwargs['wb_sizes']:
			writer.writerow([wb_size.id, wb_size.card_id, wb_size.size_name, wb_size.size_sku, wb_size.quantity, wb_size.barcode])

	with open('export.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([''])
		writer.writerow(['Изображения WB'])
		writer.writerow(['id', 'card_id', 'image_url', 'sort_order'])
		for wb_image in kwargs['wb_images']:
			writer.writerow([wb_image.id, wb_image.card_id, wb_image.image_url, wb_image.sort_order])
   
	return '.csv'

export_csv(cards=get_all_cards(), api_keys=get_api_keys(), wb_accounts=get_wb_accounts(), sync_logs=get_sync_logs(), wb_cards=get_wb_cards_by_account(1), wb_sizes=get_wb_sizes_by_card(1), wb_images=get_wb_images_by_card(1))

def export_excel(**kwargs : any) -> str:
	"""
	Экспортирует данные в Excel файл с отдельными листами для каждой таблицы
	"""
	with pd.ExcelWriter('export.xlsx', engine='openpyxl') as writer:
		# Карточки
		if 'cards' in kwargs and kwargs['cards']:
			cards_data = []
			for card in kwargs['cards']:
				cards_data.append({
					'id': card.id,
					'title': card.title,
					'description': card.description,
					'price': card.price
				})
			df_cards = pd.DataFrame(cards_data)
			df_cards.to_excel(writer, sheet_name='Карточки', index=False)
		
		# API ключи
		if 'api_keys' in kwargs and kwargs['api_keys']:
			api_keys_data = []
			for api_key in kwargs['api_keys']:
				api_keys_data.append({
					'id': api_key.id,
					'title': api_key.title,
					'api_key': api_key.api_key
				})
			df_api_keys = pd.DataFrame(api_keys_data)
			df_api_keys.to_excel(writer, sheet_name='API ключи', index=False)
		
		# Аккаунты WB
		if 'wb_accounts' in kwargs and kwargs['wb_accounts']:
			wb_accounts_data = []
			for wb_account in kwargs['wb_accounts']:
				wb_accounts_data.append({
					'id': wb_account.id,
					'title': wb_account.title,
					'api_key': wb_account.api_key,
					'account_name': wb_account.account_name,
					'company_name': wb_account.company_name,
					'is_active': wb_account.is_active,
					'created_at': wb_account.created_at,
					'last_sync': wb_account.last_sync
				})
			df_wb_accounts = pd.DataFrame(wb_accounts_data)
			df_wb_accounts.to_excel(writer, sheet_name='Аккаунты WB', index=False)
		
		# Логи синхронизации
		if 'sync_logs' in kwargs and kwargs['sync_logs']:
			sync_logs_data = []
			for sync_log in kwargs['sync_logs']:
				sync_logs_data.append({
					'id': sync_log.id,
					'account_id': sync_log.account_id,
					'status': sync_log.status,
					'cards_processed': sync_log.cards_processed,
					'error_message': sync_log.error_message,
					'sync_date': sync_log.sync_date
				})
			df_sync_logs = pd.DataFrame(sync_logs_data)
			df_sync_logs.to_excel(writer, sheet_name='Логи синхронизации', index=False)
		
		# Карточки WB
		if 'wb_cards' in kwargs and kwargs['wb_cards']:
			wb_cards_data = []
			for wb_card in kwargs['wb_cards']:
				wb_cards_data.append({
					'id': wb_card.id,
					'account_id': wb_card.account_id,
					'nm_id': wb_card.nm_id,
					'sku': wb_card.sku,
					'imt_name': wb_card.imt_name,
					'subject_name': wb_card.subject_name,
					'brand_name': wb_card.brand_name,
					'current_price': wb_card.current_price,
					'original_price': wb_card.original_price,
					'total_quantity': wb_card.total_quantity,
					'created_at': wb_card.created_at,
					'updated_at': wb_card.updated_at
				})
			df_wb_cards = pd.DataFrame(wb_cards_data)
			df_wb_cards.to_excel(writer, sheet_name='Карточки WB', index=False)
		
		# Размеры WB
		if 'wb_sizes' in kwargs and kwargs['wb_sizes']:
			wb_sizes_data = []
			for wb_size in kwargs['wb_sizes']:
				wb_sizes_data.append({
					'id': wb_size.id,
					'card_id': wb_size.card_id,
					'size_name': wb_size.size_name,
					'size_sku': wb_size.size_sku,
					'quantity': wb_size.quantity,
					'barcode': wb_size.barcode
				})
			df_wb_sizes = pd.DataFrame(wb_sizes_data)
			df_wb_sizes.to_excel(writer, sheet_name='Размеры WB', index=False)
		
		# Изображения WB
		if 'wb_images' in kwargs and kwargs['wb_images']:
			wb_images_data = []
			for wb_image in kwargs['wb_images']:
				wb_images_data.append({
					'id': wb_image.id,
					'card_id': wb_image.card_id,
					'image_url': wb_image.image_url,
					'sort_order': wb_image.sort_order
				})
			df_wb_images = pd.DataFrame(wb_images_data)
			df_wb_images.to_excel(writer, sheet_name='Изображения WB', index=False)
	
	return 'export.xlsx'

# export_excel(cards=get_all_cards(), api_keys=get_api_keys(), wb_accounts=get_wb_accounts(), sync_logs=get_sync_logs(), wb_cards=get_wb_cards_by_account(1), wb_sizes=get_wb_sizes_by_card(1), wb_images=get_wb_images_by_card(1))

