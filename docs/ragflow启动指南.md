# RAGFlow 完整操作指南

## 前置说明

| 组件 | 关系 |
|------|------|
| Docker Desktop | 容器平台，必须打开 |
| WSL | Docker 的底层引擎，自动随 Docker Desktop 启动/关闭 |
| 5 个容器 | Elasticsearch + MySQL + MinIO + Redis + RAGFlow，一条命令全起 |

**WSL 不需要手动操作，Docker Desktop 打开就自动有了。**

---

## 一、启动（每次电脑重启后）

**第 1 步**：打开 **Docker Desktop**（桌面图标或开始菜单），等右下角鲸鱼图标静止不动。

**第 2 步**：打开终端（CMD / PowerShell），粘贴并回车：

```bash
docker compose -f "D:\ragflow\ragflow-main\docker\docker-compose.yml" --profile cpu up -d && docker compose -f "D:\ragflow\ragflow-main\docker\docker-compose.yml" up -d es01
```

**第 3 步**：等 1-2 分钟，浏览器打开 **`http://127.0.0.1`**

> 开了梯子的话必须用 `127.0.0.1` 不能写 `localhost`，否则 502。

启动后 5 个容器全部 `healthy` 才算成功：

| 服务 | 作用 |
|------|------|
| es01 | Elasticsearch 搜索引擎 |
| mysql | 数据库 |
| minio | 文件存储 |
| redis | 缓存 |
| ragflow-cpu | RAGFlow 主程序 |

---

## 二、关闭（释放内存，不用的时候）

```bash
docker compose -f "D:\ragflow\ragflow-main\docker\docker-compose.yml" --profile cpu stop
```

停了再关 Docker Desktop。数据不丢。

---

## 三、查看状态

```bash
docker compose -f "D:\ragflow\ragflow-main\docker\docker-compose.yml" ps
```

看到 5 个都是 `(healthy)` 或 `Up` 就正常。
