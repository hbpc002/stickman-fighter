#!/usr/bin/env python3
"""
游戏完整性测试脚本
"""

import os
import sys

def test_files():
    """测试必要文件是否存在"""
    print("🔍 检查必要文件...")

    required_files = [
        'app.py',
        'app_enhanced.py',
        'stickman_fighter.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'deploy.sh',
        'README.md',
        'DEPLOYMENT_GUIDE.md',
        '快速开始.md',
        '.gitignore'
    ]

    missing = []
    for file in required_files:
        if os.path.exists(f'/home/hbpc/{file}'):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            missing.append(file)

    if missing:
        print(f"\n❌ 缺失文件: {missing}")
        return False

    print("\n✅ 所有必要文件都存在！")
    return True

def test_app_syntax():
    """测试Python文件语法"""
    print("\n🔍 测试Python语法...")

    files = ['app.py', 'app_enhanced.py', 'stickman_fighter.py']

    for file in files:
        try:
            with open(f'/home/hbpc/{file}', 'r', encoding='utf-8') as f:
                compile(f.read(), file, 'exec')
            print(f"  ✅ {file} 语法正确")
        except SyntaxError as e:
            print(f"  ❌ {file} 语法错误: {e}")
            return False
        except Exception as e:
            print(f"  ❌ {file} 错误: {e}")
            return False

    print("\n✅ 所有Python文件语法正确！")
    return True

def test_requirements():
    """测试requirements.txt格式"""
    print("\n🔍 检查requirements.txt...")

    try:
        with open('/home/hbpc/requirements.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' not in line and not line.startswith('-e'):
                        print(f"  ⚠️  格式警告: {line}")

        print("  ✅ requirements.txt 格式正常")
        return True
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def test_docker_files():
    """测试Docker相关文件"""
    print("\n🔍 检查Docker配置...")

    # 检查Dockerfile
    if os.path.exists('/home/hbpc/Dockerfile'):
        with open('/home/hbpc/Dockerfile', 'r') as f:
            content = f.read()
            if 'FROM python' in content and 'app.py' in content:
                print("  ✅ Dockerfile 配置正确")
            else:
                print("  ⚠️  Dockerfile 可能需要检查")
    else:
        print("  ❌ Dockerfile 不存在")
        return False

    # 检查docker-compose.yml
    if os.path.exists('/home/hbpc/docker-compose.yml'):
        print("  ✅ docker-compose.yml 存在")
    else:
        print("  ❌ docker-compose.yml 不存在")
        return False

    return True

def test_documentation():
    """测试文档完整性"""
    print("\n🔍 检查文档...")

    docs = ['README.md', 'DEPLOYMENT_GUIDE.md', '快速开始.md']

    for doc in docs:
        if os.path.exists(f'/home/hbpc/{doc}'):
            size = os.path.getsize(f'/home/hbpc/{doc}')
            if size > 100:
                print(f"  ✅ {doc} ({size} bytes)")
            else:
                print(f"  ⚠️  {doc} 内容较少")
        else:
            print(f"  ❌ {doc} 不存在")
            return False

    return True

def check_web_app_features():
    """检查Web应用特性"""
    print("\n🔍 检查Web应用特性...")

    try:
        with open('/home/hbpc/app.py', 'r', encoding='utf-8') as f:
            content = f.read()

        features = {
            'Flask路由': '@app.route' in content,
            'Canvas绘图': 'canvas' in content and 'getContext' in content,
            '键盘控制': 'keydown' in content or 'keyup' in content,
            '碰撞检测': 'checkHit' in content or 'checkCollision' in content,
            '物理系统': 'gravity' in content and ('vy' in content or 'vx' in content),
            'UI更新': 'updateUI' in content,
            '游戏循环': 'gameLoop' in content,
            'API端点': '/api/health' in content or '@app.route' in content
        }

        for feature, exists in features.items():
            status = "✅" if exists else "❌"
            print(f"  {status} {feature}")

        all_exists = all(features.values())
        if all_exists:
            print("\n✅ Web应用功能完整！")
        else:
            print("\n⚠️  部分功能可能缺失")

        return all_exists

    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def check_enhanced_features():
    """检查增强版特性"""
    print("\n🔍 检查增强版特性...")

    if not os.path.exists('/home/hbpc/app_enhanced.py'):
        print("  ⚠️  增强版文件不存在")
        return True  # 不是必须的

    try:
        with open('/home/hbpc/app_enhanced.py', 'r', encoding='utf-8') as f:
            content = f.read()

        features = {
            '连击系统': 'combo' in content,
            '特殊技能': 'special' in content or 'specialAttack' in content,
            'AI模式': 'aiControl' in content or 'aiEnabled' in content,
            '硬核模式': 'hardcore' in content,
            '音效系统': 'AudioContext' in content or 'playSound' in content,
            '增强UI': 'notification' in content,
            '统计系统': 'stats' in content
        }

        for feature, exists in features.items():
            status = "✅" if exists else "❌"
            print(f"  {status} {feature}")

        all_exists = all(features.values())
        if all_exists:
            print("\n✅ 增强版功能完整！")
        else:
            print("\n⚠️  部分增强功能可能缺失")

        return all_exists

    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🔥 火柴人对战游戏 - 完整性测试")
    print("=" * 60)

    tests = [
        ("文件完整性", test_files),
        ("Python语法", test_app_syntax),
        ("依赖配置", test_requirements),
        ("Docker配置", test_docker_files),
        ("文档完整性", test_documentation),
        ("Web应用特性", check_web_app_features),
        ("增强版特性", check_enhanced_features)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} 测试失败: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")

    print(f"\n{'=' * 60}")
    print(f"总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 恭喜！所有测试通过，游戏完整性良好！")
        print("\n🚀 下一步:")
        print("  1. 本地运行: python app.py")
        print("  2. Docker运行: docker-compose up -d")
        print("  3. 云部署: ./deploy.sh")
        print("  4. 查看文档: README.md")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查相关文件")

    print("=" * 60)

    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
