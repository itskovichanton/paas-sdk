import asyncio

from src.paassdk.eureka_session import EurekaSession


def main() -> None:
    s = EurekaSession(cherkizon_url="http://localhost:8081")
    r = s.get(url="eureka://reports[secure=false, env=dev, version=master, protocol=http]/a/b/c",
              params={"p1": 33, "p2": "dd¬"})
    print(r.text)


if __name__ == '__main__':
    main()
