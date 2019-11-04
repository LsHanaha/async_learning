
import asyncio


users = {'admin': 'admin', 'user': 'password', 'qwe': 'qwe'}
candidates = {'admin': 'admin',  '1eqw':1, 'sfsaf':54654, 'user': 'password', 'dasdsadds': 'ssfd', 'qwe': 'qwe'}


async def checking(user: str, password):
    await asyncio.sleep(5)
    if user in users and candidates[user] == users[user]:
        print(True)
    else:
        print(False)

        
async def main():
    tasks = []
    for user, password in candidates.items():
        tasks.append(checking(user, password))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

