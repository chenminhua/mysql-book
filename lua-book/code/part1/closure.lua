function newCounter()
  local count = 0
  return function()
    count = count + 1
    return count
  end
end

c = newCounter()
print(c())
print(c())
  