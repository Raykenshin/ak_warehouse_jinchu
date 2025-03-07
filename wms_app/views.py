from django.shortcuts import render, redirect
from .models import Product, wmsRecord

def scan_barcode(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        try:
            product = Product.objects.get(barcode=barcode)
            return redirect('wms_update', barcode=barcode)
        except Product.DoesNotExist:
            return render(request, 'scan_barcode.html', {'error': 'Product not found.'})
    return render(request, 'scan_barcode.html')

def wms_update(request, barcode):
    product = Product.objects.get(barcode=barcode)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        is_incoming = request.POST.get('is_incoming') == 'on'

        # 更新库存数量
        if is_incoming:
            product.stock += quantity
        else:
            if product.stock >= quantity:
                product.stock -= quantity
            else:
                return render(request, 'wms_update.html', {'product': product, 'error': 'Insufficient stock.'})
        product.save()

        wmsRecord.objects.create(product=product, quantity=quantity, is_incoming=is_incoming)
        return redirect('scan_barcode')
    return render(request, 'wms_update.html', {'product': product})