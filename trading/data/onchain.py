"""
On-Chain Data Module

Handles on-chain data fetching and analysis for CRYPTO strategies.

On-Chain Metrics:
- Exchange inflows/outflows = capital entering/leaving exchanges
- Whale transactions = large holder activity
- MVRV ratio = market top/bottom detection
- NVT = like P/E ratio for crypto

Supported APIs:
- Glassnode (mock for now)
- CryptoQuant (mock for now)

Supported Coins:
- BTC (Bitcoin)
- ETH (Ethereum)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ExchangeFlow:
    """Represents exchange inflow or outflow."""
    symbol: str
    amount: float  # Amount in coins
    value_usd: float  # Value in USD
    timestamp: datetime
    flow_type: str  # "inflow" or "outflow"
    
    def is_inflow(self) -> bool:
        """Check if this is an inflow to exchange."""
        return self.flow_type == "inflow"
    
    def is_outflow(self) -> bool:
        """Check if this is an outflow from exchange."""
        return self.flow_type == "outflow"


@dataclass
class WhaleTransaction:
    """Represents a whale transaction."""
    symbol: str
    amount: float  # Amount in coins
    value_usd: float  # Value in USD
    timestamp: datetime
    from_type: str  # "exchange", "wallet", "unknown"
    to_type: str  # "exchange", "wallet", "unknown"
    
    def is_exchange_related(self) -> bool:
        """Check if transaction involves an exchange."""
        return self.from_type == "exchange" or self.to_type == "exchange"


@dataclass
class MVRVData:
    """Represents MVRV ratio data."""
    symbol: str
    market_value: float  # Market cap (USD)
    realized_value: float  # Realized cap (USD)
    mvrv_ratio: float  # Market Value / Realized Value
    timestamp: datetime
    
    def is_overvalued(self, threshold: float = 3.0) -> bool:
        """Check if MVRV indicates overvalued market (potential top)."""
        return self.mvrv_ratio > threshold
    
    def is_undervalued(self, threshold: float = 1.0) -> bool:
        """Check if MVRV indicates undervalued market (potential bottom)."""
        return self.mvrv_ratio < threshold


@dataclass
class NVTData:
    """Represents NVT (Network Value to Transactions) ratio data."""
    symbol: str
    network_value: float  # Market cap (USD)
    transaction_volume: float  # Transaction volume (USD)
    nvt_ratio: float  # Network Value / Transaction Volume
    timestamp: datetime
    
    def is_high(self, threshold: float = 50.0) -> bool:
        """Check if NVT is high (potentially overvalued)."""
        return self.nvt_ratio > threshold
    
    def is_low(self, threshold: float = 20.0) -> bool:
        """Check if NVT is low (potentially undervalued)."""
        return self.nvt_ratio < threshold


@dataclass
class OnChainMetrics:
    """Combined on-chain metrics for a symbol."""
    symbol: str
    timestamp: datetime
    exchange_inflow_24h: float
    exchange_outflow_24h: float
    net_exchange_flow_24h: float
    whale_transaction_count_24h: int
    whale_volume_24h: float
    mvrv_ratio: float
    nvt_ratio: float
    market_cap: float
    
    def get_market_sentiment(self) -> str:
        """
        Get market sentiment based on on-chain metrics.
        
        Returns:
            Sentiment: "bullish", "bearish", or "neutral"
        """
        bullish_signals = 0
        bearish_signals = 0
        
        # Net outflow from exchanges is bullish (coins leaving exchanges)
        if self.net_exchange_flow_24h < 0:
            bullish_signals += 1
        else:
            bearish_signals += 1
        
        # Low MVRV is bullish (undervalued)
        if self.mvrv_ratio < 1.5:
            bullish_signals += 1
        elif self.mvrv_ratio > 3.0:
            bearish_signals += 1
        
        # Low NVT is bullish
        if self.nvt_ratio < 30:
            bullish_signals += 1
        elif self.nvt_ratio > 60:
            bearish_signals += 1
        
        if bullish_signals > bearish_signals:
            return "bullish"
        elif bearish_signals > bullish_signals:
            return "bearish"
        else:
            return "neutral"


class OnChainData:
    """
    Handles on-chain data for crypto trading strategies.
    
    Supports:
    - Exchange inflows/outflows tracking
    - Whale transaction detection
    - MVRV ratio calculation
    - NVT ratio calculation
    - APIs: Glassnode, CryptoQuant (mock implementations)
    - Coins: BTC, ETH
    """
    
    # Supported cryptocurrencies
    SUPPORTED_COINS = ["BTC", "ETH"]
    
    # Whale transaction threshold (in USD)
    WHALE_THRESHOLD_USD = 100000  # $100K+ transactions
    
    # MVRV thresholds
    MVRV_OVERVALUED = 3.0
    MVRV_UNDERVALUED = 1.0
    
    # NVT thresholds
    NVT_HIGH = 50.0
    NVT_LOW = 20.0
    
    def __init__(self, base_path: str = "./trading_data"):
        """
        Initialize on-chain data module.
        
        Args:
            base_path: Base path for data storage
        """
        self.base_path = Path(base_path)
        self.onchain_path = self.base_path / "onchain"
        self._ensure_directories()
        
        # In-memory caches
        self._exchange_flow_cache: Dict[str, List[ExchangeFlow]] = {}
        self._whale_cache: Dict[str, List[WhaleTransaction]] = {}
        self._mvrv_cache: Dict[str, List[MVRVData]] = {}
        self._nvt_cache: Dict[str, List[NVTData]] = {}
        
        # Current metrics cache
        self._current_metrics: Dict[str, OnChainMetrics] = {}
    
    def _ensure_directories(self):
        """Create directories if they don't exist."""
        self.onchain_path.mkdir(parents=True, exist_ok=True)
    
    def _get_filename(self, coin: str, data_type: str) -> Path:
        """Get filename for on-chain data storage."""
        return self.onchain_path / f"{data_type}_{coin.lower()}.json"
    
    # ==================== Exchange Inflows/Outflows ====================
    
    def fetch_exchange_flows(
        self, 
        coin: str, 
        days: int = 30
    ) -> List[ExchangeFlow]:
        """
        Fetch exchange inflows/outflows for a coin.
        
        This is a mock implementation. In production, this would call
        Glassnode or CryptoQuant API.
        
        Args:
            coin: Cryptocurrency symbol (BTC, ETH)
            days: Number of days to fetch
            
        Returns:
            List of ExchangeFlow objects
        """
        if coin not in self.SUPPORTED_COINS:
            raise ValueError(f"Unsupported coin: {coin}. Supported: {self.SUPPORTED_COINS}")
        
        # Check cache first
        cache_key = f"{coin}_{days}"
        if cache_key in self._exchange_flow_cache:
            return self._exchange_flow_cache[cache_key]
        
        # Try to load from storage
        flows = self._load_exchange_flows_from_storage(coin)
        
        if not flows:
            # Generate mock data for demonstration
            flows = self._generate_mock_exchange_flows(coin, days)
        
        # Cache the results
        self._exchange_flow_cache[cache_key] = flows
        
        return flows
    
    def _load_exchange_flows_from_storage(self, coin: str) -> List[ExchangeFlow]:
        """Load exchange flows from local storage."""
        filepath = self._get_filename(coin, "exchange_flows")
        
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            flows = []
            for item in data:
                flows.append(ExchangeFlow(
                    symbol=item["symbol"],
                    amount=item["amount"],
                    value_usd=item["value_usd"],
                    timestamp=datetime.fromisoformat(item["timestamp"]),
                    flow_type=item["flow_type"]
                ))
                
            return flows
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading exchange flow data for {coin}: {e}")
            return []
    
    def _generate_mock_exchange_flows(
        self, 
        coin: str, 
        days: int
    ) -> List[ExchangeFlow]:
        """Generate mock exchange flow data for testing."""
        import random
        
        flows = []
        now = datetime.now()
        
        for day in range(days):
            # Generate 1-3 flows per day
            num_flows = random.randint(1, 3)
            
            for _ in range(num_flows):
                # Random amount based on coin
                if coin == "BTC":
                    amount = random.uniform(100, 2000)  # BTC
                    price = random.uniform(60000, 100000)  # USD
                else:  # ETH
                    amount = random.uniform(1000, 20000)  # ETH
                    price = random.uniform(3000, 5000)  # USD
                
                value_usd = amount * price
                flow_type = random.choice(["inflow", "outflow"])
                
                # Timestamp within the day
                timestamp = now - timedelta(days=day, hours=random.randint(0, 23))
                
                flows.append(ExchangeFlow(
                    symbol=coin,
                    amount=amount,
                    value_usd=value_usd,
                    timestamp=timestamp,
                    flow_type=flow_type
                ))
        
        # Sort by timestamp (most recent first)
        flows.sort(key=lambda x: x.timestamp, reverse=True)
        
        return flows
    
    def get_exchange_flow_summary(self, coin: str) -> Dict[str, Any]:
        """
        Get summary of exchange flows for a coin.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            Dictionary with flow summary
        """
        flows = self.fetch_exchange_flows(coin, days=1)  # Last 24 hours
        
        inflow = sum(f.value_usd for f in flows if f.is_inflow())
        outflow = sum(f.value_usd for f in flows if f.is_outflow())
        net_flow = outflow - inflow  # Positive = net outflow (bullish)
        
        return {
            "symbol": coin,
            "inflow_24h": inflow,
            "outflow_24h": outflow,
            "net_flow_24h": net_flow,
            "flow_count": len(flows),
            "sentiment": "bullish" if net_flow > 0 else "bearish" if net_flow < 0 else "neutral"
        }
    
    # ==================== Whale Transactions ====================
    
    def fetch_whale_transactions(
        self, 
        coin: str, 
        days: int = 7
    ) -> List[WhaleTransaction]:
        """
        Fetch whale transactions for a coin.
        
        This is a mock implementation. In production, this would call
        Glassnode or CryptoQuant API.
        
        Args:
            coin: Cryptocurrency symbol (BTC, ETH)
            days: Number of days to fetch
            
        Returns:
            List of WhaleTransaction objects
        """
        if coin not in self.SUPPORTED_COINS:
            raise ValueError(f"Unsupported coin: {coin}. Supported: {self.SUPPORTED_COINS}")
        
        # Check cache first
        cache_key = f"{coin}_{days}"
        if cache_key in self._whale_cache:
            return self._whale_cache[cache_key]
        
        # Try to load from storage
        transactions = self._load_whale_transactions_from_storage(coin)
        
        if not transactions:
            # Generate mock data for demonstration
            transactions = self._generate_mock_whale_transactions(coin, days)
        
        # Cache the results
        self._whale_cache[cache_key] = transactions
        
        return transactions
    
    def _load_whale_transactions_from_storage(self, coin: str) -> List[WhaleTransaction]:
        """Load whale transactions from local storage."""
        filepath = self._get_filename(coin, "whale_transactions")
        
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            transactions = []
            for item in data:
                transactions.append(WhaleTransaction(
                    symbol=item["symbol"],
                    amount=item["amount"],
                    value_usd=item["value_usd"],
                    timestamp=datetime.fromisoformat(item["timestamp"]),
                    from_type=item["from_type"],
                    to_type=item["to_type"]
                ))
                
            return transactions
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading whale transaction data for {coin}: {e}")
            return []
    
    def _generate_mock_whale_transactions(
        self, 
        coin: str, 
        days: int
    ) -> List[WhaleTransaction]:
        """Generate mock whale transaction data for testing."""
        import random
        
        transactions = []
        now = datetime.now()
        
        for day in range(days):
            # Generate 1-5 whale transactions per day
            num_transactions = random.randint(1, 5)
            
            for _ in range(num_transactions):
                # Whale threshold amount
                if coin == "BTC":
                    amount = random.uniform(100, 500)  # BTC (100+ = $6M+)
                    price = random.uniform(60000, 100000)  # USD
                else:  # ETH
                    amount = random.uniform(500, 2000)  # ETH (500+ = $1.5M+)
                    price = random.uniform(3000, 5000)  # USD
                
                value_usd = amount * price
                
                # Only include if above whale threshold
                if value_usd < self.WHALE_THRESHOLD_USD:
                    continue
                
                # Random from/to types
                from_type = random.choice(["exchange", "wallet", "unknown"])
                to_type = random.choice(["exchange", "wallet", "unknown"])
                
                # Timestamp within the day
                timestamp = now - timedelta(days=day, hours=random.randint(0, 23))
                
                transactions.append(WhaleTransaction(
                    symbol=coin,
                    amount=amount,
                    value_usd=value_usd,
                    timestamp=timestamp,
                    from_type=from_type,
                    to_type=to_type
                ))
        
        # Sort by timestamp (most recent first)
        transactions.sort(key=lambda x: x.timestamp, reverse=True)
        
        return transactions
    
    def get_whale_activity_summary(self, coin: str) -> Dict[str, Any]:
        """
        Get summary of whale activity for a coin.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            Dictionary with whale activity summary
        """
        transactions = self.fetch_whale_transactions(coin, days=1)  # Last 24 hours
        
        exchange_related = [t for t in transactions if t.is_exchange_related()]
        total_volume = sum(t.value_usd for t in transactions)
        
        return {
            "symbol": coin,
            "whale_count_24h": len(transactions),
            "whale_volume_24h": total_volume,
            "exchange_related_count": len(exchange_related),
            "avg_transaction_size": total_volume / len(transactions) if transactions else 0,
            "whale_sentiment": "accumulation" if len(exchange_related) > len(transactions) / 2 else "distribution"
        }
    
    # ==================== MVRV Ratio ====================
    
    def fetch_mvrv_data(
        self, 
        coin: str, 
        days: int = 365
    ) -> List[MVRVData]:
        """
        Fetch MVRV ratio data for a coin.
        
        MVRV = Market Value / Realized Value
        - MVRV > 3.0: Potentially overvalued (market top)
        - MVRV < 1.0: Potentially undervalued (market bottom)
        
        This is a mock implementation. In production, this would call
        Glassnode or CryptoQuant API.
        
        Args:
            coin: Cryptocurrency symbol (BTC, ETH)
            days: Number of days to fetch
            
        Returns:
            List of MVRVData objects
        """
        if coin not in self.SUPPORTED_COINS:
            raise ValueError(f"Unsupported coin: {coin}. Supported: {self.SUPPORTED_COINS}")
        
        # Check cache first
        cache_key = f"{coin}_{days}"
        if cache_key in self._mvrv_cache:
            return self._mvrv_cache[cache_key]
        
        # Try to load from storage
        mvrv_data = self._load_mvrv_data_from_storage(coin)
        
        if not mvrv_data:
            # Generate mock data for demonstration
            mvrv_data = self._generate_mock_mvrv_data(coin, days)
        
        # Cache the results
        self._mvrv_cache[cache_key] = mvrv_data
        
        return mvrv_data
    
    def _load_mvrv_data_from_storage(self, coin: str) -> List[MVRVData]:
        """Load MVRV data from local storage."""
        filepath = self._get_filename(coin, "mvrv")
        
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            mvrv_data = []
            for item in data:
                mvrv_data.append(MVRVData(
                    symbol=item["symbol"],
                    market_value=item["market_value"],
                    realized_value=item["realized_value"],
                    mvrv_ratio=item["mvrv_ratio"],
                    timestamp=datetime.fromisoformat(item["timestamp"])
                ))
                
            return mvrv_data
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading MVRV data for {coin}: {e}")
            return []
    
    def _generate_mock_mvrv_data(
        self, 
        coin: str, 
        days: int
    ) -> List[MVRVData]:
        """Generate mock MVRV data for testing."""
        import random
        
        mvrv_data = []
        now = datetime.now()
        
        # Base values for simulation
        if coin == "BTC":
            base_market_cap = 1.2e12  # ~$1.2T
            base_realized_cap = 8e11  # ~$800B
        else:  # ETH
            base_market_cap = 4e11  # ~$400B
            base_realized_cap = 2.5e11  # ~$250B
        
        for day in range(days):
            # Simulate market cycles with some randomness
            cycle_factor = 1.0 + 0.5 * math.sin(2 * math.pi * day / 365)  # Annual cycle
            random_factor = 1.0 + random.uniform(-0.1, 0.1)
            
            market_value = base_market_cap * cycle_factor * random_factor
            realized_value = base_realized_cap * (1.0 + 0.1 * random.uniform(-0.5, 0.5))
            mvrv_ratio = market_value / realized_value
            
            timestamp = now - timedelta(days=day)
            
            mvrv_data.append(MVRVData(
                symbol=coin,
                market_value=market_value,
                realized_value=realized_value,
                mvrv_ratio=mvrv_ratio,
                timestamp=timestamp
            ))
        
        # Sort by timestamp (most recent first)
        mvrv_data.sort(key=lambda x: x.timestamp, reverse=True)
        
        return mvrv_data
    
    def get_current_mvrv(self, coin: str) -> Optional[MVRVData]:
        """
        Get current MVRV ratio for a coin.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            Current MVRVData or None if no data available
        """
        mvrv_data = self.fetch_mvrv_data(coin, days=1)
        
        if mvrv_data:
            return mvrv_data[0]
        return None
    
    def get_mvrv_signal(self, coin: str) -> Dict[str, Any]:
        """
        Get MVRV-based trading signal.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            Dictionary with signal information
        """
        current_mvrv = self.get_current_mvrv(coin)
        
        if current_mvrv is None:
            return {
                "symbol": coin,
                "mvrv_ratio": None,
                "signal": "unknown",
                "recommendation": "No MVRV data available"
            }
        
        signal = {
            "symbol": coin,
            "mvrv_ratio": current_mvrv.mvrv_ratio,
            "market_value": current_mvrv.market_value,
            "realized_value": current_mvrv.realized_value,
            "timestamp": current_mvrv.timestamp.isoformat()
        }
        
        if current_mvrv.is_overvalued(self.MVRV_OVERVALUED):
            signal["signal"] = "reversal_risk"
            signal["recommendation"] = "MVRV indicates overvalued market, consider taking profits"
        elif current_mvrv.is_undervalued(self.MVRV_UNDERVALUED):
            signal["signal"] = "accumulation"
            signal["recommendation"] = "MVRV indicates undervalued market, potential accumulation opportunity"
        else:
            signal["signal"] = "neutral"
            signal["recommendation"] = "MVRV in normal range, no clear signal"
        
        return signal
    
    # ==================== NVT Ratio ====================
    
    def fetch_nvt_data(
        self, 
        coin: str, 
        days: int = 365
    ) -> List[NVTData]:
        """
        Fetch NVT (Network Value to Transactions) ratio data for a coin.
        
        NVT = Network Value / Transaction Volume
        Similar to P/E ratio for crypto:
        - High NVT (>50): Potentially overvalued
        - Low NVT (<20): Potentially undervalued
        
        This is a mock implementation. In production, this would call
        Glassnode or CryptoQuant API.
        
        Args:
            coin: Cryptocurrency symbol (BTC, ETH)
            days: Number of days to fetch
            
        Returns:
            List of NVTData objects
        """
        if coin not in self.SUPPORTED_COINS:
            raise ValueError(f"Unsupported coin: {coin}. Supported: {self.SUPPORTED_COINS}")
        
        # Check cache first
        cache_key = f"{coin}_{days}"
        if cache_key in self._nvt_cache:
            return self._nvt_cache[cache_key]
        
        # Try to load from storage
        nvt_data = self._load_nvt_data_from_storage(coin)
        
        if not nvt_data:
            # Generate mock data for demonstration
            nvt_data = self._generate_mock_nvt_data(coin, days)
        
        # Cache the results
        self._nvt_cache[cache_key] = nvt_data
        
        return nvt_data
    
    def _load_nvt_data_from_storage(self, coin: str) -> List[NVTData]:
        """Load NVT data from local storage."""
        filepath = self._get_filename(coin, "nvt")
        
        if not filepath.exists():
            return []
        
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            nvt_data = []
            for item in data:
                nvt_data.append(NVTData(
                    symbol=item["symbol"],
                    network_value=item["network_value"],
                    transaction_volume=item["transaction_volume"],
                    nvt_ratio=item["nvt_ratio"],
                    timestamp=datetime.fromisoformat(item["timestamp"])
                ))
                
            return nvt_data
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading NVT data for {coin}: {e}")
            return []
    
    def _generate_mock_nvt_data(
        self, 
        coin: str, 
        days: int
    ) -> List[NVTData]:
        """Generate mock NVT data for testing."""
        import random
        import math
        
        nvt_data = []
        now = datetime.now()
        
        # Base values for simulation
        if coin == "BTC":
            base_network_value = 1.2e12  # ~$1.2T
        else:  # ETH
            base_network_value = 4e11  # ~$400B
        
        for day in range(days):
            # Simulate NVT cycles with some randomness
            cycle_factor = 1.0 + 0.3 * math.sin(2 * math.pi * day / 180)  # Semi-annual cycle
            random_factor = 1.0 + random.uniform(-0.15, 0.15)
            
            network_value = base_network_value * cycle_factor * random_factor
            # Transaction volume inversely related to NVT
            transaction_volume = network_value / (35 * random_factor)  # Base NVT around 35
            nvt_ratio = network_value / transaction_volume
            
            timestamp = now - timedelta(days=day)
            
            nvt_data.append(NVTData(
                symbol=coin,
                network_value=network_value,
                transaction_volume=transaction_volume,
                nvt_ratio=nvt_ratio,
                timestamp=timestamp
            ))
        
        # Sort by timestamp (most recent first)
        nvt_data.sort(key=lambda x: x.timestamp, reverse=True)
        
        return nvt_data
    
    def get_current_nvt(self, coin: str) -> Optional[NVTData]:
        """
        Get current NVT ratio for a coin.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            Current NVTData or None if no data available
        """
        nvt_data = self.fetch_nvt_data(coin, days=1)
        
        if nvt_data:
            return nvt_data[0]
        return None
    
    def get_nvt_signal(self, coin: str) -> Dict[str, Any]:
        """
        Get NVT-based trading signal.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            Dictionary with signal information
        """
        current_nvt = self.get_current_nvt(coin)
        
        if current_nvt is None:
            return {
                "symbol": coin,
                "nvt_ratio": None,
                "signal": "unknown",
                "recommendation": "No NVT data available"
            }
        
        signal = {
            "symbol": coin,
            "nvt_ratio": current_nvt.nvt_ratio,
            "network_value": current_nvt.network_value,
            "transaction_volume": current_nvt.transaction_volume,
            "timestamp": current_nvt.timestamp.isoformat()
        }
        
        if current_nvt.is_high(self.NVT_HIGH):
            signal["signal"] = "overvalued"
            signal["recommendation"] = "High NVT suggests overvaluation, be cautious"
        elif current_nvt.is_low(self.NVT_LOW):
            signal["signal"] = "undervalued"
            signal["recommendation"] = "Low NVT suggests undervaluation, potential buying opportunity"
        else:
            signal["signal"] = "neutral"
            signal["recommendation"] = "NVT in normal range, no clear signal"
        
        return signal
    
    # ==================== Combined Metrics ====================
    
    def get_onchain_metrics(self, coin: str) -> OnChainMetrics:
        """
        Get combined on-chain metrics for a coin.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            OnChainMetrics object with all metrics
        """
        # Get all metrics
        exchange_summary = self.get_exchange_flow_summary(coin)
        whale_summary = self.get_whale_activity_summary(coin)
        mvrv_signal = self.get_mvrv_signal(coin)
        nvt_signal = self.get_nvt_signal(coin)
        
        # Get current values
        current_mvrv = self.get_current_mvrv(coin)
        current_nvt = self.get_current_nvt(coin)
        
        return OnChainMetrics(
            symbol=coin,
            timestamp=datetime.now(),
            exchange_inflow_24h=exchange_summary["inflow_24h"],
            exchange_outflow_24h=exchange_summary["outflow_24h"],
            net_exchange_flow_24h=exchange_summary["net_flow_24h"],
            whale_transaction_count_24h=whale_summary["whale_count_24h"],
            whale_volume_24h=whale_summary["whale_volume_24h"],
            mvrv_ratio=mvrv_signal["mvrv_ratio"] if mvrv_signal["mvrv_ratio"] else 0.0,
            nvt_ratio=nvt_signal["nvt_ratio"] if nvt_signal["nvt_ratio"] else 0.0,
            market_cap=current_mvrv.market_value if current_mvrv else 0.0
        )
    
    def get_all_signals(self, coin: str) -> Dict[str, Any]:
        """
        Get all on-chain signals for a coin.
        
        Args:
            coin: Cryptocurrency symbol
            
        Returns:
            Dictionary with all signals
        """
        return {
            "symbol": coin,
            "timestamp": datetime.now().isoformat(),
            "exchange_flows": self.get_exchange_flow_summary(coin),
            "whale_activity": self.get_whale_activity_summary(coin),
            "mvrv_signal": self.get_mvrv_signal(coin),
            "nvt_signal": self.get_nvt_signal(coin),
            "combined_sentiment": self.get_onchain_metrics(coin).get_market_sentiment()
        }
    
    def get_all_coins_signals(self) -> Dict[str, Dict[str, Any]]:
        """
        Get on-chain signals for all supported coins.
        
        Returns:
            Dictionary mapping coin symbols to their signals
        """
        signals = {}
        
        for coin in self.SUPPORTED_COINS:
            signals[coin] = self.get_all_signals(coin)
        
        return signals
    
    # ==================== Cache Management ====================
    
    def clear_cache(self, coin: Optional[str] = None):
        """
        Clear the on-chain data cache.
        
        Args:
            coin: Specific coin to clear, or None for all
        """
        if coin:
            cache_keys_to_remove = []
            for key in self._exchange_flow_cache:
                if key.startswith(coin):
                    cache_keys_to_remove.append(key)
            for key in cache_keys_to_remove:
                del self._exchange_flow_cache[key]
            
            cache_keys_to_remove = []
            for key in self._whale_cache:
                if key.startswith(coin):
                    cache_keys_to_remove.append(key)
            for key in cache_keys_to_remove:
                del self._whale_cache[key]
            
            cache_keys_to_remove = []
            for key in self._mvrv_cache:
                if key.startswith(coin):
                    cache_keys_to_remove.append(key)
            for key in cache_keys_to_remove:
                del self._mvrv_cache[key]
            
            cache_keys_to_remove = []
            for key in self._nvt_cache:
                if key.startswith(coin):
                    cache_keys_to_remove.append(key)
            for key in cache_keys_to_remove:
                del self._nvt_cache[key]
        else:
            self._exchange_flow_cache.clear()
            self._whale_cache.clear()
            self._mvrv_cache.clear()
            self._nvt_cache.clear()


# Import math for MVRV generation
import math


# Singleton instance
_provider = None


def get_provider() -> OnChainData:
    """Get OnChainData provider instance."""
    global _provider
    if _provider is None:
        _provider = OnChainData()
    return _provider
