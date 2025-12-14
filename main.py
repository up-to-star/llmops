import uvicorn
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.http.app:app",  # 使用导入字符串引用应用
        host="0.0.0.0",
        port=8090,
        reload=True
    )
