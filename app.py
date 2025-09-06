from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# متغیرهای محیطی
PORT = int(os.environ.get('PORT', 8080))

# Health check endpoint برای Fly.io
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Expense Manager is running!",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💰 مدیریت هزینه‌های شخصی</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            
            body {
                font-family: 'Tahoma', Arial, sans-serif;
                direction: rtl;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                opacity: 0.9;
                font-size: 1.1em;
            }
            
            .content {
                padding: 40px;
            }
            
            .form-section {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 30px;
                border-left: 5px solid #667eea;
            }
            
            .form-section h3 {
                color: #333;
                margin-bottom: 20px;
                font-size: 1.4em;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            .form-row {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            
            input[type="text"], 
            input[type="number"], 
            select {
                flex: 1;
                min-width: 200px;
                padding: 15px;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                font-size: 1em;
                transition: all 0.3s ease;
            }
            
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .btn {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 1em;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 5px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            .btn-row {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .result {
                background: white;
                border: 2px solid #e9ecef;
                border-radius: 15px;
                padding: 30px;
                margin-top: 30px;
                display: none;
                animation: fadeIn 0.5s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .success { border-color: #28a745; background-color: #d4edda; }
            .error { border-color: #dc3545; background-color: #f8d7da; }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            
            .stat-value {
                font-size: 1.8em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .loading {
                display: none;
                text-align: center;
                color: #667eea;
            }
            
            @media (max-width: 600px) {
                .form-row {
                    flex-direction: column;
                }
                
                input[type="text"], 
                input[type="number"], 
                select {
                    min-width: 100%;
                }
                
                .btn-row {
                    justify-content: stretch;
                }
                
                .btn {
                    flex: 1;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💰 مدیریت هزینه‌های شخصی</h1>
                <p>به راحتی هزینه‌هایتان را مدیریت کنید</p>
            </div>
            
            <div class="content">
                <!-- Add Expense Section -->
                <div class="form-section">
                    <h3>➕ افزودن هزینه جدید</h3>
                    <div class="form-row">
                        <input type="text" id="description" placeholder="توضیحات (مثل: خرید نان)" />
                        <input type="number" id="amount" placeholder="مبلغ (تومان)" min="0" />
                        <select id="category">
                            <option value="">انتخاب دسته‌بندی</option>
                            <option value="🍽️ خوراکی">🍽️ خوراکی</option>
                            <option value="🚗 حمل‌ونقل">🚗 حمل‌ونقل</option>
                            <option value="🛍️ خرید">🛍️ خرید</option>
                            <option value="🏥 سلامت">🏥 سلامت</option>
                            <option value="🏠 خانه">🏠 خانه</option>
                            <option value="🎓 آموزش">🎓 آموزش</option>
                            <option value="🎮 تفریح">🎮 تفریح</option>
                            <option value="📝 متفرقه">📝 متفرقه</option>
                        </select>
                    </div>
                    <button class="btn" onclick="addExpense()">➕ افزودن هزینه</button>
                </div>
                
                <!-- Reports Section -->
                <div class="form-section">
                    <h3>📊 گزارش‌های هزینه</h3>
                    <div class="btn-row">
                        <button class="btn" onclick="getTotalExpenses()">💰 مجموع هزینه‌ها</button>
                        <button class="btn" onclick="getExpensesByCategory()">📊 بر حسب دسته</button>
                        <button class="btn" onclick="getRecentExpenses()">📋 هزینه‌های اخیر</button>
                        <button class="btn" onclick="getMonthlyStats()">📈 آمار ماهانه</button>
                    </div>
                </div>
                
                <!-- Loading -->
                <div id="loading" class="loading">
                    <p>⏳ در حال بارگذاری...</p>
                </div>
                
                <!-- Results -->
                <div id="result" class="result"></div>
            </div>
        </div>

        <script>
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').style.display = 'none';
            }
            
            function hideLoading() {
                document.getElementById('loading').style.display = 'none';
            }
            
            function showResult(content, isSuccess = true) {
                hideLoading();
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = content;
                resultDiv.className = 'result ' + (isSuccess ? 'success' : 'error');
                resultDiv.style.display = 'block';
                resultDiv.scrollIntoView({ behavior: 'smooth' });
            }

            async function addExpense() {
                const description = document.getElementById('description').value.trim();
                const amount = document.getElementById('amount').value;
                const category = document.getElementById('category').value;
                
                if (!description || !amount) {
                    showResult('❌ لطفاً توضیحات و مبلغ را وارد کنید', false);
                    return;
                }

                if (parseFloat(amount) <= 0) {
                    showResult('❌ مبلغ باید بیشتر از صفر باشد', false);
                    return;
                }

                showLoading();
                
                try {
                    const response = await fetch('/add_expense', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            description, 
                            amount: parseFloat(amount),
                            category: category || null
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult(`
                            <h3>✅ هزینه با موفقیت اضافه شد!</h3>
                            <p><strong>توضیحات:</strong> ${data.expense.description}</p>
                            <p><strong>مبلغ:</strong> ${data.expense.amount.toLocaleString()} تومان</p>
                            <p><strong>دسته‌بندی:</strong> ${data.expense.category}</p>
                        `);
                        
                        // Clear form
                        document.getElementById('description').value = '';
                        document.getElementById('amount').value = '';
                        document.getElementById('category').value = '';
                    } else {
                        showResult(`❌ خطا: ${data.message}`, false);
                    }
                } catch (error) {
                    showResult(`❌ خطا در اتصال: ${error.message}`, false);
                }
            }

            async function getTotalExpenses() {
                showLoading();
                try {
                    const response = await fetch('/total_expenses');
                    const data = await response.json();
                    
                    showResult(`
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-value">${data.total.toLocaleString()}</div>
                                <div>تومان</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${data.count}</div>
                                <div>تعداد هزینه</div>
                            </div>
                        </div>
                    `);
                } catch (error) {
                    showResult(`❌ خطا: ${error.message}`, false);
                }
            }

            async function getExpensesByCategory() {
                showLoading();
                try {
                    const response = await fetch('/expenses_by_category');
                    const data = await response.json();
                    
                    let content = '<h3>📊 هزینه‌ها بر حسب دسته‌بندی</h3><div class="stats-grid">';
                    
                    for (const [category, amount] of Object.entries(data)) {
                        content += `
                            <div class="stat-card">
                                <div class="stat-value">${amount.toLocaleString()}</div>
                                <div>${category}</div>
                            </div>
                        `;
                    }
                    
                    content += '</div>';
                    showResult(content);
                } catch (error) {
                    showResult(`❌ خطا: ${error.message}`, false);
                }
            }

            async function getRecentExpenses() {
                showLoading();
                try {
                    const response = await fetch('/recent_expenses');
                    const data = await response.json();
                    
                    let content = '<h3>📋 هزینه‌های اخیر</h3>';
                    
                    if (data.expenses.length === 0) {
                        content += '<p>هزینه‌ای یافت نشد.</p>';
                    } else {
                        data.expenses.forEach((expense, index) => {
                            content += `
                                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 10px; border-right: 4px solid #667eea;">
                                    <strong>${expense.description}</strong><br>
                                    <span style="color: #667eea;">💰 ${expense.amount.toLocaleString()} تومان</span>
                                    <span style="color: #6c757d; margin-right: 15px;">${expense.category}</span>
                                </div>
                            `;
                        });
                    }
                    
                    showResult(content);
                } catch (error) {
                    showResult(`❌ خطا: ${error.message}`, false);
                }
            }

            async function getMonthlyStats() {
                showLoading();
                try {
                    const response = await fetch('/monthly_stats');
                    const data = await response.json();
                    
                    showResult(`
                        <h3>📈 آمار ماهانه</h3>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-value">${data.total.toLocaleString()}</div>
                                <div>کل هزینه ماه</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${Math.round(data.average).toLocaleString()}</div>
                                <div>میانگین هزینه</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${data.count}</div>
                                <div>تعداد تراکنش</div>
                            </div>
                        </div>
                    `);
                } catch (error) {
                    showResult(`❌ خطا: ${error.message}`, false);
                }
            }
        </script>
    </body>
    </html>
    ''')

# داده‌های موقت (در پروژه واقعی از دیتابیس استفاده کنید)
expenses = []

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        amount = data.get('amount', 0)
        category = data.get('category')
        
        if not description or amount <= 0:
            return jsonify({'message': 'توضیحات و مبلغ معتبر وارد کنید'}), 400
        
        # تشخیص خودکار دسته‌بندی اگر انتخاب نشده
        if not category:
            category = categorize_expense(description)
        
        expense = {
            'id': len(expenses) + 1,
            'description': description,
            'amount': float(amount),
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        
        expenses.append(expense)
        
        return jsonify({
            'message': 'هزینه با موفقیت اضافه شد',
            'expense': expense
        })
        
    except Exception as e:
        return jsonify({'message': f'خطا در افزودن هزینه: {str(e)}'}), 500

@app.route('/total_expenses')
def total_expenses():
    total = sum(expense['amount'] for expense in expenses)
    count = len(expenses)
    return jsonify({'total': total, 'count': count})

@app.route('/expenses_by_category')
def expenses_by_category():
    categories = {}
    for expense in expenses:
        category = expense['category']
        categories[category] = categories.get(category, 0) + expense['amount']
    return jsonify(categories)

@app.route('/recent_expenses')
def recent_expenses():
    recent = expenses[-10:][::-1]  # 10 تای آخر به ترتیب معکوس
    return jsonify({'expenses': recent})

@app.route('/monthly_stats')
def monthly_stats():
    if not expenses:
        return jsonify({'total': 0, 'average': 0, 'count': 0})
    
    total = sum(expense['amount'] for expense in expenses)
    count = len(expenses)
    average = total / count if count > 0 else 0
    
    return jsonify({
        'total': total,
        'average': average,
        'count': count
    })

def categorize_expense(description):
    """تشخیص هوشمند دسته‌بندی"""
    description = description.lower()
    
    categories = {
        '🍽️ خوراکی': ['نان', 'غذا', 'رستوران', 'خوراکی', 'میوه', 'سبزیجات', 'گوشت', 'مرغ', 'لبنیات', 'شیر', 'پنیر'],
        '🚗 حمل‌ونقل': ['تاکسی', 'اتوبوس', 'مترو', 'بنزین', 'ماشین', 'موتور', 'سوخت', 'پارکینگ'],
        '🛍️ خرید': ['خرید', 'لباس', 'کفش', 'پوشاک', 'فروشگاه', 'مال', 'بازار'],                                                                          
        '🏥 سلامت': ['دارو', 'پزشک', 'دکتر', 'درمان', 'بیمارستان', 'داروخانه', 'آزمایش'],
        '🏠 خانه': ['اجاره', 'آب', 'برق', 'گاز', 'تلفن', 'اینترنت', 'خانه', 'منزل'],
        '🎓 آموزش': ['کتاب', 'دانشگاه', 'مدرسه', 'کورس', 'آموزش', 'درس'],
        '🎮 تفریح': ['سینما', 'تفریح', 'بازی', 'ورزش', 'سفر', 'کافه']
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category
    
    return '📝 متفرقه'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)                                                                                                                                                                                                                                                                                                
