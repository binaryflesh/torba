__coin__ = 'BitcoinSegwit'
__node_daemon__ = 'bitcoind'
__node_cli__ = 'bitcoin-cli'
__node_url__ = (
    'https://bitcoin.org/bin/bitcoin-core-0.16.0/bitcoin-0.16.0-x86_64-linux-gnu.tar.gz'
)

from six import int2byte
from binascii import unhexlify
from torba.baseledger import BaseLedger, BaseHeaders
from torba.basenetwork import BaseNetwork
from torba.basescript import BaseInputScript, BaseOutputScript
from torba.basetransaction import BaseTransaction, BaseInput, BaseOutput
from torba.basecoin import BaseCoin
from torba.basedatabase import BaseSQLiteWalletStorage
from torba.basemanager import BaseWalletManager


class WalletManager(BaseWalletManager):
    pass


class SQLiteWalletStorage(BaseSQLiteWalletStorage):
    pass


class Input(BaseInput):
    script_class = BaseInputScript


class Output(BaseOutput):
    script_class = BaseOutputScript


class Transaction(BaseTransaction):
    input_class = Input
    output_class = Output


class BitcoinSegwitLedger(BaseLedger):
    network_class = BaseNetwork
    headers_class = BaseHeaders


class MainNetLedger(BitcoinSegwitLedger):
    pass


class UnverifiedHeaders(BaseHeaders):
    verify_bits_to_target = False


class RegTestLedger(BitcoinSegwitLedger):
    headers_class = UnverifiedHeaders
    max_target = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    genesis_hash = '0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206'
    genesis_bits = 0x207fffff
    target_timespan = 1
    verify_bits_to_target = False


class BitcoinSegwit(BaseCoin):
    name = 'BitcoinSegwit'
    symbol = 'BTC'
    network = 'mainnet'

    ledger_class = MainNetLedger
    transaction_class = Transaction

    pubkey_address_prefix = int2byte(0x00)
    script_address_prefix = int2byte(0x05)
    extended_public_key_prefix = unhexlify('0488b21e')
    extended_private_key_prefix = unhexlify('0488ade4')

    default_fee_per_byte = 50

    def __init__(self, ledger, fee_per_byte=default_fee_per_byte):
        super(BitcoinSegwit, self).__init__(ledger, fee_per_byte)


class BitcoinSegwitRegtest(BitcoinSegwit):
    network = 'regtest'
    ledger_class = RegTestLedger