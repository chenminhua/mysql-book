network = {
  {name="grauna", IP="210.26.30.34"},
  {name="lua", IP="232.32.23.23"}
}

table.sort(network, function(a,b) return (a.name > b.name) end)

function derivative(f, delta)
  delta = delta or 1e-4
  return function(x)
    return (f(x+delta) - f(x)) / delta
  end
end

c = derivative(math.sin)
print(math.cos(10), c(10))
