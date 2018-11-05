from django.shortcuts import render, get_object_or_404, redirect
from contracts.models import Contract
from .forms import PaymentForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse
from .models import Payment
from django.contrib.auth.decorators import login_required
from account.permission_decortor import accountant_only


@login_required
def payment_detail(request, contract_id):
    """
    根据合同ID返回指定合同的付款详情页
    页面内包含该合同的简要数据以及付款记录
    :param request:
    :param contract_id:
    :return:
    """
    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        payments = contract.payments.all()
        form = PaymentForm()
        return render(request, 'payments/payment_detail.html',
                      {'contract': contract, 'payments': payments, 'form': form})
    else:
        # if not request.user.is_accountant:
        #     raise PermissionDenied
        contract = get_object_or_404(Contract, id=contract_id)
        payments = contract.payments.all()
        form = PaymentForm(request.POST)
        if form.is_valid():
            new_payment = form.save(commit=False)
            new_payment.contract = contract
            new_payment.save()
            messages.success(request, '成功添加付款记录')
            return redirect(reverse('payments:payment_detail', args=[contract.id]))
        else:
            return render(request, 'payments/payment_detail.html',
                          {"contract": contract, 'payments': payments, 'form': form})


@login_required
# @accountant_only
def payment_edit(request, contract_id, payment_id):
    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        payment = get_object_or_404(Payment, id=payment_id)
        form = PaymentForm(instance=payment)
        return render(request, 'payments/payment_edit.html', {'contract': contract, 'form': form})

    else:
        contract = get_object_or_404(Contract, id=contract_id)
        payment = get_object_or_404(Payment, id=payment_id)
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            current_payment = form.save(commit=False)
            current_payment.contract = contract
            current_payment.save()
            messages.success(request, '修改付款记录成功')
            return redirect(reverse('payments:payment_detail', args=[contract.id]))
        else:
            return render(request, 'payments/payment_detail.html', {'contract': contract, 'form': form})
