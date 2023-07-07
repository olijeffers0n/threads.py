import requests


class ThreadsClient:

    async def _get_lsd(self) -> str:
        response = requests.get("https://www.threads.net/@instagram")
        if response.status_code != 200:
            return None

        content = response.text
        i = content.find("\"token\"")
        if i == -1:
            return None

        return content[i + 9: i + 31]

    async def get_user(self, user_id: int) -> dict:
        lsd = await self._get_lsd()
        response = requests.post(f"https://www.threads.net/api/graphql", headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "X-IG-App-ID": "238260118697367",
            "X-FB-LSD": lsd,
            "Sec-Fetch-Site": "same-origin",
        }, data={
            "lsd": lsd,
            "variables": f'{{"userID":"{user_id}"}}',
            "doc_id": "23996318473300828"
        })
        if response.status_code != 200:
            return None

        return response.json()

    async def get_post(self, post_id):
        lsd = await self._get_lsd()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-IG-App-ID": "238260118697367",
            "X-FB-LSD": lsd,
            "Sec-Fetch-Site": "same-origin"
        }

        data = {
            "lsd": lsd,
            "variables": f'{{"postID":"{post_id}"}}',
            "doc_id": "5587632691339264"
        }

        response = requests.post("https://www.threads.net/api/graphql", headers=headers, data=data)

        if response.status_code != 200:
            return None

        return response.json()
