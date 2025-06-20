from datetime import datetime
from pytz import timezone, utc

def convert_utc_to_fuso_brasilia(dt_utc):
    '''
        função para converter um datetime em UTC para o fuso de Brasília(América/Sao_Paulo)
        Retorna o datetime ajustado com o timezone de Brasília
    '''
    if dt_utc is None:
        return None
    
    adjust_timezone_brasilia = timezone('America/Sao_Paulo')
    return dt_utc.replace(tzinfo=utc).astimezone(adjust_timezone_brasilia)

