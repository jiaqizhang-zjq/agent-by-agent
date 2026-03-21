---
name: "service-deploy"
description: "本地部署和启动Agent服务。当用户提到部署、启动服务、编译、build、重启服务、部署出错、服务起不来时调用。"
---

# 服务部署器

这个Skill用于本地部署和启动Agent服务。

## 何时调用

在以下情况下调用此Skill：
- 用户要求"部署服务"
- 用户要求"启动服务"
- 用户要求"编译"或"build"
- 用户要求"重启服务"
- 用户提到"部署出错"
- 用户提到"服务起不来"

## 核心功能

### 1. 完整部署流程

**三步构建流程：**

```
步骤1：环境检查
├── 检查依赖项
├── 检查配置文件
├── 检查端口占用
└── 检查权限

步骤2：构建编译
├── 安装依赖
├── 编译代码
├── 打包资源
└── 生成配置

步骤3：启动服务
├── 启动进程
├── 健康检查
├── 日志收集
└── 状态监控
```

### 2. 环境检查

**检查清单：**

#### 依赖检查
- [ ] Python版本（3.8+）
- [ ] Node.js版本（16+）
- [ ] 必要的系统库
- [ ] 第三方依赖包

#### 配置检查
- [ ] 配置文件存在
- [ ] 配置项完整
- [ ] 配置格式正确
- [ ] 敏感信息加密

#### 环境检查
- [ ] 端口可用
- [ ] 文件权限
- [ ] 磁盘空间
- [ ] 内存充足

### 3. 部署脚本

**自动化部署脚本：**

```bash
#!/bin/bash

# 服务部署脚本

# 1. 环境检查
echo "=== 步骤1：环境检查 ==="
check_dependencies() {
    echo "检查依赖..."
    # 检查Python
    python --version || { echo "Python未安装"; exit 1; }
    # 检查依赖包
    pip install -r requirements.txt || { echo "依赖安装失败"; exit 1; }
}

# 2. 构建编译
echo "=== 步骤2：构建编译 ==="
build_service() {
    echo "构建服务..."
    # 编译代码
    python setup.py build || { echo "构建失败"; exit 1; }
    # 打包资源
    python setup.py install || { echo "安装失败"; exit 1; }
}

# 3. 启动服务
echo "=== 步骤3：启动服务 ==="
start_service() {
    echo "启动服务..."
    # 启动进程
    nohup python main.py > logs/service.log 2>&1 &
    # 健康检查
    sleep 5
    curl http://localhost:8000/health || { echo "服务启动失败"; exit 1; }
}

# 主流程
main() {
    check_dependencies
    build_service
    start_service
    echo "=== 部署完成 ==="
}

main
```

### 4. 常见问题排查

**问题诊断清单：**

#### 端口占用
```bash
# 检查端口占用
lsof -i :8000

# 杀掉占用进程
kill -9 <PID>
```

#### 权限问题
```bash
# 检查文件权限
ls -la

# 修改权限
chmod +x script.sh
```

#### 依赖缺失
```bash
# 检查依赖
pip list

# 安装缺失依赖
pip install -r requirements.txt
```

#### 配置错误
```bash
# 检查配置文件
cat config.yaml

# 验证配置格式
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

### 5. 远程调试部署

**远程调试指南：**

#### SSH连接
```bash
# 连接远程服务器
ssh user@remote-server

# 上传代码
scp -r ./local-code user@remote-server:/remote-path
```

#### 远程调试
```bash
# 启动远程调试
python -m pdb main.py

# 查看日志
tail -f logs/service.log

# 检查进程
ps aux | grep python
```

#### 性能监控
```bash
# CPU使用率
top

# 内存使用
free -h

# 磁盘使用
df -h
```

## 部署流程

### 步骤1：准备阶段

```
1. 收集部署信息
   - 服务名称
   - 部署环境
   - 配置要求

2. 检查环境
   - 依赖检查
   - 配置检查
   - 权限检查

3. 准备资源
   - 代码打包
   - 配置文件
   - 启动脚本
```

### 步骤2：部署阶段

```
1. 执行部署
   - 安装依赖
   - 编译代码
   - 配置服务

2. 启动服务
   - 启动进程
   - 健康检查
   - 日志收集

3. 验证部署
   - 功能测试
   - 性能测试
   - 稳定性测试
```

### 步骤3：监控阶段

```
1. 状态监控
   - 进程状态
   - 资源使用
   - 错误日志

2. 性能监控
   - 响应时间
   - 吞吐量
   - 错误率

3. 告警设置
   - 异常告警
   - 性能告警
   - 资源告警
```

## 部署检查清单

### 部署前检查
- [ ] 代码已提交
- [ ] 配置已更新
- [ ] 依赖已安装
- [ ] 端口已检查

### 部署中检查
- [ ] 构建成功
- [ ] 配置正确
- [ ] 进程启动
- [ ] 健康检查通过

### 部署后检查
- [ ] 服务可访问
- [ ] 功能正常
- [ ] 性能达标
- [ ] 日志正常

## 常见问题解决

### 问题1：端口被占用

**症状：**
```
Error: Address already in use
```

**解决方案：**
```bash
# 查找占用进程
lsof -i :8000

# 杀掉进程
kill -9 <PID>

# 或修改端口
export PORT=8001
```

### 问题2：依赖缺失

**症状：**
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案：**
```bash
# 安装依赖
pip install xxx

# 或安装所有依赖
pip install -r requirements.txt
```

### 问题3：权限不足

**症状：**
```
PermissionError: [Errno 13] Permission denied
```

**解决方案：**
```bash
# 修改权限
chmod +x script.sh

# 或使用sudo
sudo python main.py
```

### 问题4：配置错误

**症状：**
```
ConfigError: Invalid configuration
```

**解决方案：**
```bash
# 检查配置文件
cat config.yaml

# 验证配置格式
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

## 最佳实践

### 1. 自动化部署
- 使用脚本自动化
- 版本控制配置
- 回滚机制

### 2. 监控告警
- 实时监控
- 及时告警
- 快速响应

### 3. 日志管理
- 集中收集
- 定期归档
- 便于排查

### 4. 安全加固
- 最小权限
- 敏感信息加密
- 访问控制

## 输出内容

此Skill将生成：
- **部署脚本**：自动化部署脚本
- **检查报告**：环境检查报告
- **部署日志**：部署过程日志
- **问题诊断**：问题诊断报告

## 注意事项

- **备份配置**：部署前备份配置
- **测试验证**：部署后测试验证
- **监控告警**：设置监控告警
- **文档记录**：记录部署过程

## 权限说明

作为服务部署器，我有权限：
- 执行部署脚本
- 修改配置文件
- 启动/停止服务
- 收集日志信息
- 执行系统命令
