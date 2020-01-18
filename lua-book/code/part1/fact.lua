function fact(n)
  if n == 0 then
    return 1
  else
    return n * fact(n-1)
  end
end

function norm(x, y)
  return (x^2 + y^2)^0.5
end

function twice(x)
  return 2 * x
end

print("enter a number:")
a = io.read("*number")
print(fact(a))