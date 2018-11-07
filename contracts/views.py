from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, Contract
from .forms import ContractForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# 自定义权限管理的装饰器：
from account.permission_decortor import contractor_only

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='cmslog.log',
    filemode='a+')


def contract_list(request, subject_id=None):
    subject = None
    if request.method == "GET":
        subjects = Subject.objects.all().order_by('created')
        contracts = Contract.objects.filter(master__isnull=True)
        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id)
            contracts = contracts.filter(subject=subject)
        return render(request,
                      'contracts/contracts_list.html',
                      {'subjects': subjects,
                       'contracts': contracts,
                       'subject': subject})

    else:
        search = request.POST.get('search', None)
        if not search:
            return redirect(reverse('contracts:contract_list'))
        subjects = Subject.objects.all().order_by('created')
        contracts = Contract.objects.filter(
            Q(name__contains=search) | Q(supplier__contains=search)).distinct()
        return render(request,
                      'contracts/contracts_search.html',
                      {'subjects': subjects,
                       'contracts': contracts,
                       'search': search})


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request,
                  'contracts/contracts_detail.html',
                  {'contract': contract})


@login_required
# @contractor_only
def contract_add(request, master_id=None):
    contract = None
    if request.method == 'GET':
        form = ContractForm()
        if master_id:
            contract = get_object_or_404(Contract, id=master_id)
            if contract.is_supple():
                messages.error(request, '您正在为一个补充合同添加补充合同！')
        return render(request, 'contracts/contracts_add.html',
                      {'form': form, 'contract': contract})

    else:
        form = ContractForm(request.POST)
        if form.is_valid():
            new_contract = form.save(commit=False)
            index = new_contract.company.name + '(' + new_contract.sign.strftime(
                "%Y") + ')' + '-' + new_contract.subject.tag + '-' + str(
                Contract.objects.filter(subject=new_contract.subject).filter(master__isnull=True).count() + 1).zfill(4)
            master_contract_id = request.POST.get('master', None)
            if master_contract_id:
                new_contract.master = int(master_contract_id)
                supple_count = Contract.objects.filter(
                    master=int(master_contract_id)).count()
                index = Contract.objects.get(
                    id=new_contract.master).index + '-补-' + str(supple_count + 1).zfill(4)
            new_contract.index = index
            new_contract.save()
            logging.info(
                "{} | contract_add | name={} | id={}".format(
                    request.user.username,
                    new_contract.name,
                    new_contract.id))
            messages.success(request, '合同新增成功')
            return redirect(
                reverse(
                    'contracts:contract_detail',
                    args=[
                        new_contract.id]))
        messages.error(request, '请检查填写是否正确')
        return render(request, 'contracts/contracts_add.html', {'form': form})


@login_required
# @contractor_only
def contract_edit(request, contract_id):
    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        form = ContractForm(instance=contract)
        return render(request, 'contracts/contracts_edit.html',
                      {'form': form, 'contract': contract})

    else:
        contract = get_object_or_404(Contract, id=contract_id)
        form = ContractForm(request.POST, instance=contract)
        index = contract.index
        master = contract.master
        if form.is_valid():
            current_contract = form.save(commit=False)
            current_contract.index = index
            current_contract.master = master
            current_contract.save()
            logging.info(
                "{} | contract_edit | name={} | id={}".format(
                    request.user.username,
                    current_contract.name,
                    current_contract.id))
            messages.success(request, '合同信息修改成功')
            return redirect(
                reverse(
                    'contracts:contract_detail',
                    args=[
                        contract.id]))
        messages.error(request, '请检查填写是否正确')
        return render(request, 'contracts/contracts_edit.html',
                      {'form': form, 'contract': contract})
