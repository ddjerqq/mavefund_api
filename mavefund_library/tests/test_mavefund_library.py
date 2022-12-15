from mavefund_library.src import Client

client = Client("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDUyMjY3NDY5NDAyNzE2NzAiLCJleHAiOjE2NzA5NTQ2MjR9.sLL62bbTHjcw0Fa19RtQ7Bo5w1k6BWXD3EzHhtjqnNw")

# TODO this is getting imported while we are running other tests.
data = client.get_records_as_df("AAPL")
print(data)
