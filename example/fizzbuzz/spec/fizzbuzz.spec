
$import
    import target
$end
$describe "test"
    $subject "test"
    $end

$end

$describe "test"
$end

$describe "Hello Hello Hello Hello"
$end



$describe "test"
    $subject
        into code
    $end
$end

$describe "test"
    $subject
        return target.fizzbuzz(n())
    $end
    $describe ""
        $describe "test"
        $end
        $describe "test"

        $end
        $example "return 1"
            assert subject() == "1"
        $end
        $let "n"
            return 1
        $end
    $end

    $describe ""
        $let "n"
            return 3
        $end
        $example "calling Fizz"
            assert subject() == "Fizz"
        $end
    $end
    $describe "when n eq 5"
        $let "n"
            return 5
        $end
        $example "Hello"
            assert subject() == "Buzz"

        $end
    $end
    $describe "when n eq 30"
        $let "n"
            return 30
        $end
        $example "calling FizzBuzz"
            assert subject() == "FizzBuzz"
        $end
    $end
$end