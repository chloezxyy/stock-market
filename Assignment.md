# Assignment – Super Simple Stock Market

# **Requirements**

1. The Global Beverage Corporation Exchange is a new stock market trading in drinks companies.  
   1. Your company is building the object-oriented system to run that trading.   
   2. You have been assigned to build part of the core object model for a limited phase 1  
2. Provide the complete source code that will:-  
   1. For a given stock,   
      1. Given any price as input, calculate the dividend yield  
      2. Given any price as input,  calculate the P/E Ratio  
      3. Record a trade, with timestamp, quantity, buy or sell indicator and price  
      4. Calculate Volume Weighted Stock Price based on trades in past  5 minutes  
   2. Calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks

# **Constraints & Notes**

1. Written in one of these languages \- Java, C\#, C++, Python  
2. The source code should be suitable for forming part of the object model of a production application, and can be proven to meet the requirements. A shell script is not an appropriate submission for this assignment.   
3. No database, GUI or I/O is required, all data need only be held in memory  
4. No prior knowledge of stock markets or trading is required – all formulas are provided below.  
5. The code should provide only the functionality requested, however it must be production quality.

### **Table1. Sample data from the Global Beverage Corporation Exchange**

| Stock Symbol | Type | Last Dividend | Fixed Dividend | Par Value |  |
| :---- | :---- | ----: | ----: | ----: | :---- |
| **TEA** | Common | 0 |  | 100 |  |
| **POP** | Common | 8 |  | 100 |  |
| **ALE** | Common | 23 |  | 60 |  |
| **GIN** | Preferred | 8 | 2% | 100 |  |
| **JOE** | Common | 13 |  | 250 |  |
| *All number values in pennies* |  |  |  |  |  |

### **Table 2\. Formula**

|  | Common | Preferred |
| :---- | :---: | :---: |
| Dividend Yield | Last DividendPrice | Fixed Dividend .Par ValuePrice |
| P/E Ratio | PriceDividend |  |
| Geometric Mean | np1p2p3pn |  |
| Volume Weighted Stock Price | i Traded PriceiQuantityiiQuantityi |  |

V1.7