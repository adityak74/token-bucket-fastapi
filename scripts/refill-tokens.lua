-- refill token script
local bucket_size_key = KEYS[1]
local current_bucket_size = tonumber(redis.call("GET", bucket_size_key))

local total_bucket_size = tonumber(ARGV[1])
local refill_size = tonumber(ARGV[2])

if current_bucket_size < (total_bucket_size - refill_size) then
    if current_bucket_size < 0 then
        redis.call("SET", bucket_size_key, total_bucket_size)
    else
        redis.call("SET", bucket_size_key, current_bucket_size + refill_size)
    end
end

return { current_bucket_size }
