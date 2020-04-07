Twitter clone https://github.com/antirez/retwis , http://retwis.redis.io/ , https://redis.io/topics/twitter-clone , https://docs.spring.io/spring-data/data-keyvalue/examples/retwisj/current/

What keys are needed to represent our objects and what kind of values this keys need to hold.

## Users

{username, userid, password, set(following), set(follower)}

userId 从哪儿来？可以考虑使用 INCR 操作，建一个 string 类型的值叫 next_user_id

用 hash 存 User, key 为 user:id,比如 INCR 返回 1000，那么 key 就是 user:1000

HMSET user:1000 username cmh password pwd

注意，我们还要用一个 hashmap，因为我们可能会需要从用户名来查用户 id，所以等于是用 hashmap 建一个关于名字的索引。

HSET users cmh 1000

## Followers, Following

用两个 Sorted Set 吧，这样能知道关注时间。

followers:1000 => Sorted Set of uids of all the followers users
following:1000 => Sorted Set of uids of all the following users

ZINTERSTORE 可以用来找到两个人的共同好友

## Timelines

We need to access this data in chronological order later, so we use list.
Lpushed new update, LRange data.

## Post

Incr next_post_id => 10343
Hmset post:10343 user_id 1000 time 12121212 body “hello world”
Zrange followers:1000 0 -1 拿到所有 follower
Foreach lpush timeline:followerid 10343 推到每个 follower 的 timeline 里面

LRANGE is not very efficient if the list of posts start to be very big, and we want to access elements which are in the middle of the list,
since Redis Lists are backed by linked lists. If a system is designed for deep pagination of million of items, it is better to resort to Sorted Sets instead.

## Authentication

HSET user:1000 auth fea5e81ac8ca77622bed1c2132a021f9
HSET auths fea5e81ac8ca77622bed1c2132a021f9
Logout and expire

Making it horizontally scalable

On a very slow and loaded server, an Apache benchmark with 100 parallel clients issuing 100000 requests measured the average pageview to take 5 milliseconds. This means you can serve millions of users every day with just a single Linux box,However you can't go with a single server forever, how do you scale a key-value store?
Retwis does not perform any multi-keys operation, so making it scalable is simple: you may use client-side sharding, or something like a sharding proxy like Twemproxy, or the upcoming Redis Cluster.
To know more about those topics please read our documentation about sharding. However, the point here to stress is that in a key-value store, if you design with care, the data set is split among many independent small keys. To distribute those keys to multiple nodes is more straightforward and predictable compared to using a semantically more complex database system.
