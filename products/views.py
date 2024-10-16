from django.http import JsonResponse
from django.views import View

# Sample product data
products = [
    {'id': 1, 'name': 'Product 1', 'category': 'Category A', 'price': 100},
    {'id': 2, 'name': 'Product 2', 'category': 'Category B', 'price': 150},
    {'id': 3, 'name': 'Product 3', 'category': 'Category A', 'price': 200},
    {'id': 4, 'name': 'Product 4', 'category': 'Category C', 'price': 50},
]

class ProductListView(View):
    def get(self, request):
        # Get query parameters
        product_id = request.GET.get('id')
        category = request.GET.get('category')
        sort_by = request.GET.get('sort_by', 'id')
        order = request.GET.get('order', 'asc')

        # Initialize filtered products
        filtered_products = products

        # Validate product ID
        if product_id:
            if not product_id.isdigit() or int(product_id) not in [p['id'] for p in products]:
                return JsonResponse({'error': 'Invalid product ID.'}, status=400)
            filtered_products = [p for p in products if p['id'] == int(product_id)]
        
        # Filter products by category
        elif category:
            filtered_products = [p for p in products if p['category'] == category]

        # Sort products
        if sort_by in ['id', 'name', 'price']:
            filtered_products = sorted(filtered_products, key=lambda x: x[sort_by], reverse=(order == 'desc'))
        else:
            return JsonResponse({'error': 'Invalid sort parameter.'}, status=400)

        return JsonResponse(filtered_products, safe=False)
