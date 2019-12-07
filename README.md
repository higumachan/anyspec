# anysepc

このリポジトリはRubyのRspecに似た記法でテストを書くことができるDSLと各言語に対してコンパイル(トランスパイル)するバックエンド。

# How to use

## Python

pythonでspecを書く

target.py
```python
def fizzbuzz(n):
    if n % 5 == 0 and n % 3 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

fizzbuzz.spec
```
$import! 
    import target
$end

$describe "fizzbuzz"
    subject! 
        target.fizzbuzz(n())
    $end
    $describe "when n == 1"
        $it "return 1"
            assert subject() == "1"
        $end
    $end
    $describe "when n == 3"
        $it "calling Fizz"
            assert subject() == "Fizz"
        $end
    $end
    $describe "when n == 5"
        $it "calling Buzz"
            assert subject() == "Buzz"
        $end
    $end   
    $describe "when n == 30"
        $it "calling FizzBuzz"
            assert subject() == "FizzBuzz"
        $end
    $end   
$end
```

その後にasc.pyでコンパイル(トランスパイル)する。

```shell script
python asc.py fizzbuzz.spec tests
```

`./tests`にfizzbuzz.pyというファイルができる。

これを`pytest`実行することでテストができる。

```shell script
pytest tests
```
