# app/main.py 
from flask import Flask, request, jsonify
from scanner.scan import ContractScanner

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_contract():
    # 获取上传的文件
    file = request.files['file']
    # 有一个函数来获取文件的路径
    contract_path = get_contract_path(file)
    # 创建扫描器实例
    scanner = ContractScanner(contract_path)
    # 执行扫描
    results = scanner.scan()
    
    # 准备响应数据
    response = {
        'issues': [str(issue) for issue in results.issues]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)