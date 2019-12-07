$import
    import target
$end

$describe "fizzbuzz"
    $subject
        return target.fizzbuzz(n())
    $end
    $describe "when n eq 1"
        $let "n"
            return 1
        $end
        $it "return 1"
            assert subject() == "1"
        $end
    $end
    $describe "when n eq 3"
        $let "n"
            return 3
        $end
        $it "calling Fizz"
            assert subject() == "Fizz"
        $end
    $end
    $describe "when n eq 5"
        $let "n"
            return 5
        $end
        $it "calling Buzz"
            assert subject() == "Buzz"
        $end
    $end
    $describe "when n eq 30"
        $let "n"
            return 30
        $end
        $it "calling FizzBuzz"
            assert subject() == "FizzBuzz"
        $end
    $end
$end