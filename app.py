import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from transitions.extensions import GraphMachine

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

API_TOKEN = '<Token>'
WEBHOOK_URL = '<URL>' + '/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)

chat_dict = {}
machines = {};
m_homo_list = []
m_hetero_list = []
f_homo_list = []
f_hetero_list = []
secret_list = []

keyboard1 = [
		[
			KeyboardButton(text="男生"),
			KeyboardButton(text="女生"),
			KeyboardButton(text="不告訴你")
			]
		]
keyboard2 = [
		[
			KeyboardButton(text="男生"),
			KeyboardButton(text="女生"),
			]
		]

reply_markup1 = ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=False, one_time_keyboard=True)
reply_markup2 = ReplyKeyboardMarkup(keyboard=keyboard2, resize_keyboard=False, one_time_keyboard=True)

class TocMachine(GraphMachine):
	def __init__(self, **machine_configs):
		self.machine = GraphMachine(
			model = self,
			**machine_configs
		)

	def is_going_to_male(self, update):
		text = update.message.text
		return text == '男生'

	def is_going_to_female(self, update):
		text = update.message.text
		return text == '女生'

	def is_going_to_secret(self, update):
		text = update.message.text
		return text == '不告訴你'

	def is_going_to_m_homo(self, update):
		text = update.message.text
		return text == '男生'
	
	def is_going_to_m_hetero(self, update):
		text = update.message.text
		return text == '女生'

	def is_going_to_f_homo(self, update):
		text = update.message.text
		return text == '女生'

	def is_going_to_f_hetero(self, update):
		text = update.message.text
		return text == '男生'

	def is_going_to_chat(self, update):
		return str(update.message.chat.id) in chat_dict

	def is_going_to_start(self, update):
		text = update.message.text
		if text == '/離開':
			return True
		else:
			another_id = chat_dict[str(update.message.chat.id)]
			bot.sendMessage(chat_id=another_id, text=text)
			return False

	def is_stopping_search(self, update):
		text = update.message.text
		chat_id = update.message.chat.id
		if text == '/停止':
			if chat_id in m_homo_list:
				print('\tRemove ' + str(chat_id) + ' from m_homo_list')
				m_homo_list.remove(chat_id)
			elif chat_id in m_hetero_list:
				print('\tRemove ' + str(chat_id) + ' from m_hetero_list')
				m_hetero_list.remove(chat_id)
			elif chat_id in f_homo_list:
				print('\tRemove ' + str(chat_id) + ' from f_homo_list')
				f_homo_list.remove(chat_id)
			elif chat_id in f_hetero_list:
				print('\tRemove ' + str(chat_id) + ' from f_hetero_list')
				f_hetero_list.remove(chat_id)
			elif chat_id in secret_list:
				print('\tRemove ' + str(chat_id) + ' from secret_list')
				secret_list.remove(chat_id)
			return True
		else:
			return False

	def on_enter_male(self, update):
		bot.sendMessage(chat_id=update.message.chat.id, text='想要跟誰聊天？', reply_markup=reply_markup2)

	def on_enter_female(self, update):
		bot.sendMessage(chat_id=update.message.chat.id, text='想要跟誰聊天？', reply_markup=reply_markup2)


	def on_enter_m_homo(self, update):
		bot.sendMessage(chat_id=update.message.chat.id, text='尋人中，請稍候……\n\n（輸入「/停止」中斷搜尋。）', reply_markup=ReplyKeyboardRemove())
		if len(m_homo_list) < 1:
			print('\tAdd ' + str(update.message.chat.id) + ' to m_homo_list')
			m_homo_list.append(update.message.chat.id)
		else:
			another_id = m_homo_list[0]
			print('\tRemove ' + str(another_id) + ' from m_homo_list')
			del m_homo_list[0]
			print('\tAdd ' + str(update.message.chat.id) + ' to chat_dict')
			chat_dict[str(update.message.chat.id)] = another_id
			print('\tAdd ' + str(another_id) + ' to chat_dict')
			chat_dict[str(another_id)] = update.message.chat.id
			self.advance(update)
			update.message.chat.id = another_id
			machines[str(another_id)].advance(update)
		print_population()

	def on_enter_m_hetero(self, update):
		bot.sendMessage(chat_id=update.message.chat.id, text='尋人中，請稍候……\n\n（輸入「/停止」中斷搜尋。）', reply_markup=ReplyKeyboardRemove())
		if len(f_hetero_list) < 1:
			print('\tAdd ' + str(update.message.chat.id) + ' to m_hetero_list')
			m_hetero_list.append(update.message.chat.id)
		else:
			another_id = f_hetero_list[0]
			print('\tRemove ' + str(another_id) + ' from f_hetero_list')
			del f_hetero_list[0]
			print('\tAdd ' + str(update.message.chat.id) + ' to chat_dict')
			chat_dict[str(update.message.chat.id)] = another_id
			print('\tAdd ' + str(another_id) + ' to chat_dict')
			chat_dict[str(another_id)] = update.message.chat.id
			self.advance(update)
			update.message.chat.id = another_id
			machines[str(another_id)].advance(update)
		print_population()

	def on_enter_f_homo(self, update):
		bot.sendMessage(chat_id=update.message.chat.id, text='尋人中，請稍候……\n\n（輸入「/停止」中斷搜尋。）', reply_markup=ReplyKeyboardRemove())
		if len(f_homo_list) < 1:
			print('\tAdd ' + str(update.message.chat.id) + ' to f_homo_list')
			f_homo_list.append(update.message.chat.id)
		else:
			another_id = f_homo_list[0]
			print('\tRemove ' + str(another_id) + ' from f_homo_list')
			del f_homo_list[0]
			print('\tAdd ' + str(update.message.chat.id) + ' to chat_dict')
			chat_dict[str(update.message.chat.id)] = another_id
			print('\tAdd ' + str(another_id) + ' to chat_dict')
			chat_dict[str(another_id)] = update.message.chat.id
			self.advance(update)
			update.message.chat.id = another_id
			machines[str(another_id)].advance(update)
		print_population()

	def on_enter_f_hetero(self, update):
		bot.sendMessage(chat_id=update.message.chat.id, text='尋人中，請稍候……\n\n（輸入「/停止」中斷搜尋。）', reply_markup=ReplyKeyboardRemove())
		if len(m_hetero_list) < 1:
			print('\tAdd ' + str(update.message.chat.id) + ' to f_hetero_list')
			f_hetero_list.append(update.message.chat.id)
		else:
			another_id = m_hetero_list[0]
			print('\tRemove ' + str(another_id) + ' from m_hetero_list')
			del m_hetero_list[0]
			print('\tAdd ' + str(update.message.chat.id) + ' to chat_dict')
			chat_dict[str(update.message.chat.id)] = another_id
			print('\tAdd ' + str(another_id) + ' to chat_dict')
			chat_dict[str(another_id)] = update.message.chat.id
			self.advance(update)
			update.message.chat.id = another_id
			machines[str(another_id)].advance(update)
		print_population()
			
	def on_enter_secret(self, update):
		bot.sendMessage(chat_id=update.message.chat.id, text='尋人中，請稍候……\n\n（輸入「/停止」中斷搜尋。）', reply_markup=ReplyKeyboardRemove())
		if len(secret_list) < 1:
			print('\tAdd ' + str(update.message.chat.id) + ' to secret_list')
			secret_list.append(update.message.chat.id)
		else:
			another_id = secret_list[0]
			print('\tRemove ' + str(another_id) + ' from secret_list')
			del secret_list[0]
			print('\tAdd ' + str(update.message.chat.id) + ' to chat_dict')
			chat_dict[str(update.message.chat.id)] = another_id
			print('\tAdd ' + str(another_id) + ' to chat_dict')
			chat_dict[str(another_id)] = update.message.chat.id
			self.advance(update)
			update.message.chat.id = another_id
			machines[str(another_id)].advance(update)
		print_population()

	def on_enter_chat(self, update):
		update.message.reply_text("配對成功，可以開始聊天囉！\n\n（輸入「/離開」來離開對話。）")
		print_population()

	def on_exit_chat(self, update):
		if str(update.message.chat.id) in chat_dict:
			bot.sendMessage(chat_id=update.message.chat.id, text='您已退出聊天。')
			chat_id = update.message.chat.id
			another_id = chat_dict[str(chat_id)]
			print('\tRemove ' + str(another_id) + ' from chat_dict')
			del chat_dict[str(another_id)]
			print('\tRemove ' + str(chat_id) + ' from chat_dict')
			del chat_dict[str(chat_id)]
			update.message.chat.id = another_id
			machines[str(another_id)].advance(update)
			update.message.chat.id = chat_id
		else:
			bot.sendMessage(chat_id=update.message.chat.id, text='對方已退出聊天。')

	def on_enter_start(self, update):
		chat_id=update.message.chat.id
		bot.sendMessage(chat_id=chat_id, text='欸欸')
		bot.sendMessage(chat_id=chat_id, text='你是男生女生？')
		bot.sendMessage(chat_id=chat_id, text='（目前 '
				+ str(len(m_homo_list) + len(m_hetero_list)) + '男 '
				+ str(len(f_homo_list) + len(f_hetero_list)) + '女 '
				+ str(len(secret_list)) + '未知 等待中。）', reply_markup=reply_markup1)
		print_population()

def _set_webhook():
	status = bot.set_webhook(WEBHOOK_URL)
	if not status:
		print('Webhook setup failed')
		sys.exit(1)
	else:
		print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))

def print_population():
	print('\tCurrent Population: chat=' + str(len(chat_dict))
			+ ', m_homo='+ str(len(m_homo_list))
			+ ', m_hetero='+ str(len(m_hetero_list))
			+ ', f_homo='+ str(len(f_homo_list))
			+ ', f_hetero='+ str(len(f_hetero_list))
			+ ', secret='+ str(len(secret_list))
			)

@app.route('/hook', methods=['POST'])
def webhook_handler():
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	chat_id = update.message.chat.id
	if str(chat_id) not in machines:
		print('\tNew user added, id= ' + str(chat_id))
		machines[str(chat_id)] = TocMachine(
				states=[
					'start',
					'male',
					'female',
					'secret',
					'm_homo',
					'm_hetero',
					'f_homo',
					'f_hetero',
					'chat'
					],
				transitions=[
					{
						'trigger': 'advance',
						'source': 'start',
						'dest': 'male',
						'conditions': 'is_going_to_male'
						},
					{
						'trigger': 'advance',
						'source': 'start',
						'dest': 'female',
						'conditions': 'is_going_to_female'
						},
					{
						'trigger': 'advance',
						'source': 'start',
						'dest': 'secret',
						'conditions': 'is_going_to_secret'
						},
					{
						'trigger': 'advance',
						'source': 'male',
						'dest': 'm_homo',
						'conditions': 'is_going_to_m_homo'
						},
					{
						'trigger': 'advance',
						'source': 'male',
						'dest': 'm_hetero',
						'conditions': 'is_going_to_m_hetero'
						},
					{
						'trigger': 'advance',
						'source': 'female',
						'dest': 'f_homo',
						'conditions': 'is_going_to_f_homo'
						},
					{
						'trigger': 'advance',
						'source': 'female',
						'dest': 'f_hetero',
						'conditions': 'is_going_to_f_hetero'
						},
					{
						'trigger': 'advance',
						'source': [
							'm_homo',
							'm_hetero',
							'f_homo',
							'f_hetero',
							'secret'
							],
						'dest': 'start',
						'conditions': 'is_stopping_search'
						},
					{
						'trigger': 'advance',
						'source': [
							'm_homo',
							'm_hetero',
							'f_homo',
							'f_hetero',
							'secret'
							],
						'dest': 'chat',
						'conditions': 'is_going_to_chat'
						},

					{
						'trigger': 'advance',
						'source': 'chat',
						'dest': 'start',
						'conditions': 'is_going_to_start'
						}
					],
				initial='start',
				auto_transitions=False,
				show_conditions=True,
				)
		bot.sendMessage(chat_id=chat_id, text='欸欸')
		bot.sendMessage(chat_id=chat_id, text='你是男生女生？')
		bot.sendMessage(chat_id=chat_id, text='（目前 '
				+ str(len(m_homo_list) + len(m_hetero_list)) + '男 '
				+ str(len(f_homo_list) + len(f_hetero_list)) + '女 '
				+ str(len(secret_list)) + '未知 等待中。）', reply_markup=reply_markup1)
	machines[str(chat_id)].advance(update)
	return 'ok'

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
	byte_io = BytesIO()
	machines[str(list(machines.keys())[0])].graph.draw(byte_io, prog='dot', format='png')
	byte_io.seek(0)
	return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

if __name__ == "__main__":
	_set_webhook()
	app.run()
