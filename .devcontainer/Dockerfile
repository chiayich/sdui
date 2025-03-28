FROM python:3.11-bullseye

# 使用清华大学的Debian镜像源
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 安装基础工具
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    curl \
    git \
    vim \
    htop \
    jq \
    less \
    ssh \
    iputils-ping \
    net-tools \
    sudo \
    gnupg \
    lsb-release \
    wget \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# 安装NodeJS (使用官方方式但配置淘宝镜像)
ENV NODE_VERSION=18.x
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - \
    && apt-get update && apt-get install -y nodejs \
    && npm config set registry https://registry.npmmirror.com

# 安装TypeScript和Vue CLI
RUN npm install -g typescript @vue/cli

# 安装Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 配置pip使用清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装开发依赖
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    black \
    flake8 \
    pylint \
    pytest \
    pytest-cov \
    pre-commit \
    httpie \
    datamodel-code-generator \
    fastapi \
    uvicorn[standard] \
    sqlalchemy \
    psycopg2-binary \
    redis

# 配置环境
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 

# 设置vscode用户
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m vscode \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# 添加vscode用户到docker组
RUN groupadd -g 997 docker || true \
    && usermod -aG docker vscode

ENV PATH="/home/vscode/.local/bin:${PATH}"

# 配置git使用国内镜像(可选)
RUN git config --global url."https://gitclone.com/github.com/".insteadOf "https://github.com/"

# 设置工作目录
WORKDIR /workspace

USER vscode 