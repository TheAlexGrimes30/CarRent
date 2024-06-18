import logging
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
logging.basicConfig(filename=BASE_DIR / 'logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger()
