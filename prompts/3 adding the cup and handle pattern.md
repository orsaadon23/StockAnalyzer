# Adding Cup and Handle Pattern Detection

I need to implement a cup and handle pattern detection algorithm for stock prices. This pattern is a bullish continuation pattern that looks like a "U" shape (the cup) followed by a small downward drift (the handle).

Please help me implement this in the existing stock analysis system. The implementation should:

1. Add a new endpoint `/cup-and-handle/{symbol}` to the Flask API
2. Implement the pattern detection algorithm that:
   - Analyzes historical price data for the given stock symbol
   - Identifies a U-shaped price trajectory (the cup)
   - Detects a small downward/sideways consolidation period (the handle)
   - Calculates pattern strength based on volume and price movement
3. Return a JSON response with:
   - Boolean indicating if pattern is detected
   - Pattern strength score (0-100)
   - Start and end dates of the pattern
   - Key price levels (cup bottom, handle top, etc.)

The implementation should be efficient and handle edge cases appropriately. Please ensure the code is clean, well-documented, and follows best practices.
