fn main() raises:
    print("Hello from Mojo!")
    
    # This is a sample Mojo function
    fn fibonacci(n: Int) -> Int:
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    # Test the function
    var result = fibonacci(10)
    print("Fibonacci(10) =", result) 