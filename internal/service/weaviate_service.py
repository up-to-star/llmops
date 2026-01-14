import weaviate


client = weaviate.connect_to_custom(
    skip_init_checks=False,
    http_host="127.0.0.1",
    http_port=18080,
    http_secure=False,
    grpc_host="127.0.0.1",
    grpc_port=50051,
    grpc_secure=False
)


# 检查连接是否成功
print(client.is_ready())

# 关闭连接
print(client.close())