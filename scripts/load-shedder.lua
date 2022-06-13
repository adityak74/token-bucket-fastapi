math.randomseed(os.time())

request = function()
    url_path = "/load?q=" .. math.random(0, 1)
    return wrk.format("GET", url_path)
end
