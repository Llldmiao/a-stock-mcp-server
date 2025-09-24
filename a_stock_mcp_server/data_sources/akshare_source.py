"""
AKShare数据源实现
"""

import logging
from typing import Dict, Any
import pandas as pd

from .base import BaseDataSource, DataSourceConfig

logger = logging.getLogger(__name__)


class AKShareDataSource(BaseDataSource):
    """AKShare数据源"""
    
    def __init__(self, config: DataSourceConfig = None):
        if config is None:
            config = DataSourceConfig(
                name="akshare",
                enabled=True,
                priority=1,
                timeout=30,
                retry_count=3,
                cache_ttl=300
            )
        super().__init__(config)
    
    async def get_realtime_price(self, symbol: str) -> Dict[str, Any]:
        """获取实时价格"""
        try:
            import akshare as ak
            
            # 获取实时行情
            stock_realtime = ak.stock_zh_a_spot_em()
            
            # 查找指定股票
            stock_data = stock_realtime[stock_realtime["代码"] == symbol]
            
            if stock_data.empty:
                raise ValueError(f"未找到股票代码: {symbol}")
            
            stock_info = stock_data.iloc[0]
            
            return {
                "symbol": self._safe_get_field(stock_info, '代码', symbol),
                "name": self._safe_get_field(stock_info, '名称', 'N/A'),
                "current_price": self._safe_get_field(stock_info, '最新价'),
                "change": self._safe_get_field(stock_info, '涨跌额', 0),
                "change_percent": self._safe_get_field(stock_info, '涨跌幅'),
                "volume": self._safe_get_field(stock_info, '成交量'),
                "turnover": self._safe_get_field(stock_info, '成交额'),
                "high": self._safe_get_field(stock_info, '最高'),
                "low": self._safe_get_field(stock_info, '最低'),
                "open": self._safe_get_field(stock_info, '今开'),
                "prev_close": self._safe_get_field(stock_info, '昨收'),
                "turnover_rate": self._safe_get_field(stock_info, '换手率'),
                "pe_ratio": self._safe_get_field(stock_info, '市盈率-动态', 'N/A'),
                "pb_ratio": self._safe_get_field(stock_info, '市净率', 'N/A'),
                "timestamp": self._safe_get_field(stock_info, '时间', 'N/A'),
                "source": "akshare"
            }
            
        except ImportError:
            raise ImportError("AKShare未安装，请运行 pip install akshare")
        except Exception as e:
            self.logger.error(f"获取实时价格失败: {e}")
            raise
    
    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """获取股票基本信息"""
        try:
            import akshare as ak
            
            # 获取股票基本信息
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            
            info_dict = {}
            for _, row in stock_info.iterrows():
                info_dict[row['item']] = row['value']
            
            return {
                "symbol": symbol,
                "info": info_dict,
                "source": "akshare"
            }
            
        except ImportError:
            raise ImportError("AKShare未安装，请运行 pip install akshare")
        except Exception as e:
            self.logger.error(f"获取股票信息失败: {e}")
            raise
    
    async def get_market_summary(self) -> Dict[str, Any]:
        """获取市场概况"""
        try:
            import akshare as ak
            
            # 获取大盘指数
            index_data = ak.stock_zh_index_spot_em()
            
            summary = []
            for _, row in index_data.iterrows():
                summary.append({
                    "name": row['名称'],
                    "price": row['最新价'],
                    "change": row['涨跌额'],
                    "change_percent": row['涨跌幅']
                })
            
            return {
                "summary": summary,
                "source": "akshare"
            }
            
        except ImportError:
            raise ImportError("AKShare未安装，请运行 pip install akshare")
        except Exception as e:
            self.logger.error(f"获取市场概况失败: {e}")
            raise
    
    async def get_stock_history(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取股票历史数据"""
        try:
            import akshare as ak
            
            period = kwargs.get("period", "daily")
            start_date = kwargs.get("start_date", "20240101")
            end_date = kwargs.get("end_date", "20241231")
            
            # 获取历史数据
            hist_data = ak.stock_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            
            if hist_data.empty:
                raise ValueError(f"未找到 {symbol} 的历史数据")
            
            # 转换为字典列表
            history = []
            for _, row in hist_data.iterrows():
                history.append({
                    "date": str(row['日期']),
                    "open": row['开盘'],
                    "close": row['收盘'],
                    "high": row['最高'],
                    "low": row['最低'],
                    "volume": row['成交量'],
                    "turnover": row['成交额']
                })
            
            return {
                "symbol": symbol,
                "period": period,
                "start_date": start_date,
                "end_date": end_date,
                "history": history,
                "source": "akshare"
            }
            
        except ImportError:
            raise ImportError("AKShare未安装，请运行 pip install akshare")
        except Exception as e:
            self.logger.error(f"获取历史数据失败: {e}")
            raise
    
    async def get_financial_data(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取财务数据"""
        try:
            import akshare as ak
            
            report_type = kwargs.get("report_type", "income")
            
            if report_type == "income":
                # 利润表
                financial_data = ak.stock_financial_abstract(symbol=symbol)
            elif report_type == "balance":
                # 资产负债表
                financial_data = ak.stock_balance_sheet_by_report_em(symbol=symbol)
            elif report_type == "cashflow":
                # 现金流量表
                financial_data = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
            else:
                raise ValueError("不支持的财务数据类型")
            
            if financial_data.empty:
                raise ValueError(f"未找到 {symbol} 的财务数据")
            
            return {
                "symbol": symbol,
                "report_type": report_type,
                "data": financial_data.to_dict('records'),
                "source": "akshare"
            }
            
        except ImportError:
            raise ImportError("AKShare未安装，请运行 pip install akshare")
        except Exception as e:
            self.logger.error(f"获取财务数据失败: {e}")
            raise
    
    def _safe_get_field(self, data: Any, field: str, default: Any = "N/A") -> Any:
        """安全获取字段值"""
        try:
            if hasattr(data, "get"):
                return data.get(field, default)
            elif hasattr(data, field):
                return getattr(data, field, default)
            else:
                return default
        except (KeyError, AttributeError):
            return default
