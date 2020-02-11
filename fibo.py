print("Fibonacci analysis")

def fibo(n):
    result = [1,1]
    for i in range(n-2):
        result.append(result[i] + result[(i+1)])
    print(result)

fibo(18)