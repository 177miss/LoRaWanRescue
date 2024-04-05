import time
from django.core.management.base import BaseCommand
from appexpress import stream
     
class Command(BaseCommand):
    help = 'Runs a background task'
    
    def handle(self, *args, **options):
        # 添加延迟，单位为秒
        #time.sleep(5)  # 延迟 60 秒
        # 在这里调用你的后台任务函数 
        stream
