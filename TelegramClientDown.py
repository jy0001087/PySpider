from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterVideo, InputMessagesFilterMusic
import os
import asyncio
import logging
from telethon.utils import get_input_location

# 请在这里填写你的API ID和API Hash
api_id = '25270021'
api_hash = 'e27d91ad37959d54eb5c1d454d567afa'

# 你想要下载视频的Telegram群组或频道用户名
group_username =  -1001981879084

# 视频保存目录
download_path = 'D:\\TelegramDownloads'

# 确保保存目录存在
if not os.path.exists(download_path):
    os.makedirs(download_path)

# 设置日志配置
log_file_path = os.path.join(download_path, 'log.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 创建一个Telethon客户端
client = TelegramClient('session_name', api_id, api_hash)


async def download_file(semaphore,message, download_path):
    """
    下载单个文件的函数
    """
    async with semaphore:
        if message.media:
            # 获取文件名，如果没有则使用消息ID
            file_name = message.file.name or f"{message.id}.mp4"
            save_path = os.path.join(download_path, file_name)
            if os.path.exists(save_path):
                logging.info(f"文件已存在，跳过: {file_name}")
                return

            # 获取文件大小并记录到日志
            file_size = message.file.size if message.file else 0
            if message.video:
                file_size = message.video.size
            elif message.audio:
                file_size = message.audio.size

            logging.info(f"++++++++正在下载文件: {file_name} 大小: {file_size / (1024 * 1024):.2f} MB")

            # 定义进度回调函数，带文件名区分
            def progress_callback(current, total):
                percentage = (current * 100 / total) if total else 0
                logging.info(f"########文件 {file_name}: 下载进度 {percentage:.2f}%")

            await message.download_media(file=save_path,progress_callback=progress_callback)

            logging.info(f"--------下载完成: {file_name}")

async def main():
    # 连接到Telegram服务器
    await client.start()

    # 获取群组或频道的实体
    group = await client.get_entity(group_username)

    # 获取所有文件、音频和视频消息
    messages_files = await client.get_messages(group, None, filter=InputMessagesFilterDocument)
    messages_videos = await client.get_messages(group, None, filter=InputMessagesFilterVideo)
    messages_audios = await client.get_messages(group, None, filter=InputMessagesFilterMusic)

    # 将所有消息合并到一个列表中
    all_messages = messages_files + messages_videos + messages_audios

# 创建Semaphore，限制同时进行的任务数为2
    semaphore = asyncio.Semaphore(10)
    # 创建任务列表
    tasks = [download_file(semaphore, message, download_path) for message in all_messages]

    # 并行执行所有下载任务
    await asyncio.gather(*tasks)

    logging.info("所有文件下载完成。")

# 启动事件循环并运行下载任务
with client:
    client.loop.run_until_complete(main())