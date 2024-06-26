# coding: utf-8

COMPANY_CODE = {'005930': ['삼성전자', 'sec'], '373220': ['LG에너지솔루션', 'lgenergy'], 
        '000660': ['SK하이닉스', 'skhynix'], '207940': ['삼성바이오로직스', 'ssbio'],
        '006400': ['삼성SDI', 'sdi'], '051910': ['LG화학', 'lgchemical'],
        '005935': ['삼성전자우', 'secpre'], '005380': ['현대차', 'hyunmotor'],
        '035420': ['NAVER', 'naver'], '000270': ['기아', 'kia'],
        '035720': ['카카오', 'kakao'], '005490': ['POSCO홀딩스', 'poscoholding'],
        '105560': ['KB금융', 'kbbank'], '028260': ['삼성물산', 'sscnt'],
        '068270': ['셀트리온', 'celltrion'], '012330': ['현대모비스', 'mobis'],
        '055550': ['신한지주', 'shgroup'], '066570': ['LG전자', 'lgelec'],
        '003670': ['포스코퓨처엠', 'poscochemical'], '096770': ['SK이노베이션', 'skinnovation'],
        '033780': ['KT&G', 'ktng'], '030200': ['KT', 'kt'],
        '003550': ['LG', 'lg'], '034730': ['SK', 'sk'], 
        '032830': ['삼성생명', 'sslife'], '086790': ['하나금융지주', 'hana'], 
        '009150': ['삼성전기', 'sselec'], '015760': ['한국전력', 'koreaelec'],
        '034020': ['두산에너빌리티', 'doosanener'], '010130': ['고려아연', 'koreazinc'],
        '017670': ['SK텔레콤', 'sktelecom'], '011200': ['HMM', 'hmm'],
        '000810': ['삼성화재', 'ssfire'], '051900': ['LG생활건강', 'lglife'],
        '010950': ['S-Oil', 'soil'], '259960': ['크래프톤', 'crafton'],
        '018260': ['삼성에스디에스', 'sds'], '329180': ['현대중공업', 'hhi'],
        '003490': ['대한항공', 'koreanair'], '036570': ['엔씨소프트', 'ncsoft'],
        '009830': ['한화솔루션', 'hanhwasol'], '316140': ['우리금융지주', 'woorifg'],
        '090430': ['아모레퍼시픽', 'amore'], '011170': ['롯데케미칼', 'lottechem'], 
        '024110': ['기업은행', 'ibk'], '138040': ['메리츠금융지주', 'meritz'], 
        '377300': ['카카오페이', 'kakaopay'], '011070': ['LG이노텍', 'lginnotek'],
        '028050': ['삼성엔지니어링', 'ssengineering'], '361610': ['SK아이이테크놀로지', 'skietech'],
        '086280': ['현대글로비스', 'glovis'], '302440': ['SK바이오사이언스', 'skbio'],
       }

US_SECTOR_LIST = [['^SP500-40',  'spsy',  'spsy.pkl'], ['^GSPE', 'spny', 'spny.pkl'], ['^SP500-35', 'spxhc', 'spxhc.pkl'],
                  ['^SP500-25', 'splrcd', 'splrcd.pkl'], ['^SP500-20', 'splrci', 'splrci.pkl'], ['^SP500-55', 'splrcu', 'splrcu.pkl'],
                  ['^SP500-30', 'splrcs', 'splrcs.pkl'], ['^SP500-45', 'splrct', 'splrct.pkl'], ['^SP500-50', 'splrcl', 'splrcl.pkl'],
                  ['^SP500-15', 'splrcm', 'splrcm.pkl'], ['^BANK', 'ixbk', 'ixbk.pkl'], ['^OFIN', 'ixfn', 'ixfn.pkl'],
                  ['^INDS', 'ixid', 'ixid.pkl'], ['^INSR', 'ixis', 'ixis.pkl'], ['^IXCO', 'ixk', 'ixk.pkl'], 
                  ['^TRAN', 'ixtr', 'ixtr.pkl'], ['^IXTC', 'ixut', 'ixut.pkl'], ['^NBI', 'nbi', 'nbi.pkl'], ['^BKX', 'bkx', 'bkx.pkl']]

HEADERS = {'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_11_5) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}