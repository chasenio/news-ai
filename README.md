# Finance News

## Task

| Section         | Task                         | Time | Status |
|-----------------|------------------------------|------|--------|
| config          | load yaml                    |      | x      |
|                 | load from consul             |      | x      |
| database        | design model                 |      | x      |
|                 | migration                    |      | x      |
|                 | news control (find, save)    |      | x      |
| rest api        | list days                    |      | x      |
|                 | list article                 |      | x      |
|                 | search article               |      | x      |
|                 | ai summary news              |      | x      |
| spider          | thread loop                  |      | x      |
|                 | parser bloomberg             |      | x      |
|                 | parser barron                |      | x      |
| ai summary call | research                     |      | x      |
|                 | stream response              |      | x      |
| web page        | list article                 |      | x      |
|                 | search bar                   |      | x      |
|                 | ai summary news              |      | x      |
|                 | ~~more news~~                |      |        |
| deploy          | deploy backend with fly.io   |      | x      |
|                 | deploy front with cloudflare |      | x      |


## api

- /news/<day> 查看某一天的新闻, 搜索新闻
- /ai/<day> 使用 ai 总结指定天的新闻


## services ops
```shell
# attach consul
fly consul attach -a news-ai
# ssh virtual machine console
fly ssh console -a news-ai
```

