export const strategyDetails: { [key: string]: any } = {
    "sma_crossover": {
        description: "A simple strategy that generates buy/sell signals based on the crossover of two Simple Moving Averages (SMAs) of different lengths. When the shorter-term SMA crosses above the longer-term SMA, it's a buy signal. When it crosses below, it's a sell signal.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Price',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Short SMA',
                    data: [60, 62, 68, 75, 65, 60, 50],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                },
                {
                    label: 'Long SMA',
                    data: [50, 55, 60, 65, 70, 68, 65],
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'SMA Crossover Example'
                }
            }
        }
    },
    "adaptive_strategy": {
        description: "A strategy that adapts to changing market conditions by adjusting its parameters based on market volatility.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Price',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Adaptive MA',
                    data: [62, 60, 75, 78, 60, 58, 45],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'Adaptive Strategy Example'
                }
            }
        }
    },
    "rsi": {
        description: "A momentum oscillator that measures the speed and change of price movements. It is used to identify overbought or oversold conditions.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'RSI',
                    data: [75, 80, 85, 70, 60, 40, 30],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Overbought (70)',
                    data: [70, 70, 70, 70, 70, 70, 70],
                    borderColor: 'rgb(255, 99, 132)',
                    borderDash: [5, 5],
                    pointRadius: 0
                },
                {
                    label: 'Oversold (30)',
                    data: [30, 30, 30, 30, 30, 30, 30],
                    borderColor: 'rgb(54, 162, 235)',
                    borderDash: [5, 5],
                    pointRadius: 0
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'RSI Example'
                }
            }
        }
    },
    "macd": {
        description: "A trend-following momentum indicator that shows the relationship between two moving averages of a security's price.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'MACD Line',
                    data: [1, 1.5, 2, 1, 0, -1, -0.5],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Signal Line',
                    data: [0.5, 0.8, 1.2, 1.1, 0.8, 0.2, 0],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'MACD Example'
                }
            }
        }
    },
    "bollinger_bands": {
        description: "A volatility indicator that consists of a middle band (a simple moving average) and two outer bands that are typically two standard deviations away from the middle band.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Price',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Upper Band',
                    data: [75, 70, 90, 92, 68, 65, 50],
                    borderColor: 'rgb(255, 99, 132)',
                    borderDash: [5, 5],
                    pointRadius: 0
                },
                {
                    label: 'Lower Band',
                    data: [55, 48, 70, 70, 44, 45, 30],
                    borderColor: 'rgb(54, 162, 235)',
                    borderDash: [5, 5],
                    pointRadius: 0
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'Bollinger Bands Example'
                }
            }
        }
    },
    "ema_crossover": {
        description: "Similar to the SMA Crossover, but uses Exponential Moving Averages (EMAs) which give more weight to recent prices.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Price',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Short EMA',
                    data: [62, 61, 70, 78, 68, 62, 52],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                },
                {
                    label: 'Long EMA',
                    data: [55, 57, 62, 68, 70, 69, 66],
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'EMA Crossover Example'
                }
            }
        }
    },
    "stochastic_oscillator": {
        description: "A momentum indicator that compares a particular closing price of a security to a range of its prices over a certain period of time.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: '%K',
                    data: [80, 85, 90, 75, 65, 50, 40],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: '%D',
                    data: [75, 80, 85, 80, 75, 65, 55],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'Stochastic Oscillator Example'
                }
            }
        }
    },
    "ichimoku_cloud": {
        description: "A collection of indicators that show support and resistance levels, as well as momentum and trend direction.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Price',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Conversion Line',
                    data: [60, 62, 68, 75, 65, 60, 50],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                },
                {
                    label: 'Base Line',
                    data: [50, 55, 60, 65, 70, 68, 65],
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'Ichimoku Cloud Example'
                }
            }
        }
    },
    "vwap": {
        description: "Volume-Weighted Average Price (VWAP) is a trading benchmark that gives the average price a security has traded at throughout the day, based on both volume and price.",
        chartData: {
            labels: ['09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30'],
            datasets: [
                {
                    label: 'Price',
                    data: [100, 102, 101, 103, 102, 104, 105],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'VWAP',
                    data: [100.5, 101.2, 101.5, 102.3, 102.5, 103.1, 103.8],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'VWAP Example'
                }
            }
        }
    },
    "mean_reversion": {
        description: "A strategy that assumes that a stock's price will tend to move back to the average price over time.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Price',
                    data: [65, 59, 80, 81, 56, 55, 40],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Mean',
                    data: [60, 60, 60, 60, 60, 60, 60],
                    borderColor: 'rgb(255, 99, 132)',
                    borderDash: [5, 5],
                    pointRadius: 0
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'Mean Reversion Example'
                }
            }
        }
    },
    "momentum": {
        description: "A strategy that aims to capitalize on the continuance of existing trends in the market.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Price',
                    data: [40, 45, 55, 65, 80, 85, 90],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'Momentum Example'
                }
            }
        }
    },
    "awesome_oscillator": {
        description: "An indicator used to measure market momentum. It is calculated as the difference between a 34-period and a 5-period simple moving average.",
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [
                {
                    label: 'Awesome Oscillator',
                    data: [1, 1.5, 2, 1, 0, -1, -0.5],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    backgroundColor: (context: any) => {
                        const value = context.dataset.data[context.dataIndex];
                        return value >= 0 ? 'rgba(75, 192, 192, 0.5)' : 'rgba(255, 99, 132, 0.5)';
                    },
                    type: 'bar'
                }
            ]
        },
        chartOptions: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top' as const,
                },
                title: {
                    display: true,
                    text: 'Awesome Oscillator Example'
                }
            }
        }
    }
};