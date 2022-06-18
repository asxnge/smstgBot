import psutil

text_info = """
<b>💻 Информация о системе:</b>

<b>Кол-во ядер:</b>  {core}
<b>Кол-во ОЗУ:</b>  {memory} МБ

<b>Загруженность ОЗУ:</b>  {memory_load} %
<b>Загруженность ЦП:</b>  {core_load} %
"""


class System:
    @staticmethod
    def info_msg():
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_amount = '{:.2f}'.format(memory.total / 1024 / 1024)

        text = text_info.format(core=psutil.cpu_count(), memory=memory_amount,
                            memory_load=memory_percent, core_load=cpu)

        return text
