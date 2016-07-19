require 'sinatra'
require 'json'
require 'net/http'
require 'rubygems'


@user = 'mozilla-bot'
@pass = '!Test1234'
@host = 'https://api.github.com'

@post_ws = "/repos/SebastinSanty/potential-octo-doodle/issues/1/comments"

@payload ={
    "body" => "Hello",
  }.to_json
  
def poster
	req = Net::HTTP::Post.new(@post_ws, initheader = {'Content-Type' =>'application/json'})
          req.basic_auth @user, @pass
          req.body = @payload
          response = Net::HTTP.new(@host, @port).start {|http| http.request(req) }
           puts "Response #{response.code} #{response.message}:
          #{response.body}"
        end

thepost = poster
puts thepost

post '/payload' do
  push = JSON.parse(request.body.read)
  puts "I got some JSON: #{push.inspect}"
end