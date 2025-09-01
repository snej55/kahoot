require 'net/http'
require 'json'

uri = URI.parse('https://randomuser.me/api')
response = Net::HTTP.get_response(uri)
data = JSON.parse(response.body)

t = Time.now.to_i

puts t