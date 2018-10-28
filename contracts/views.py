from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, Contract
from .forms import ContractForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def contract_list(request, subject_id=None):
    subject = None
    if request.method == "GET":
        subjects = Subject.objects.all().order_by('created')
        contracts = Contract.objects.all()
        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id)
            contracts = contracts.filter(subject=subject)
        return render(request, 'contracts/contracts_list.html',
                      {'subjects': subjects, 'contracts': contracts, 'subject': subject})

    else:
        print('收到POST请求,待开发查询功能')
        subjects = Subject.objects.all().order_by('created')
        contracts = Contract.objects.all()
        return render(request, 'contracts/contracts_list.html',
                      {'subjects': subjects, 'contracts': contracts})


def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    return render(request, 'contracts/contracts_detail.html', {'contract': contract})


@login_required
def contract_add(request, master_id=None):
    contract = None
    if request.method == 'GET':
        form = ContractForm()
        if master_id:
            contract = get_object_or_404(Contract, id=master_id)
        return render(request, 'contracts/contracts_add.html', {'form': form, 'contract': contract})

    else:
        form = ContractForm(request.POST)
        if form.is_valid():
            new_contract = form.save(commit=False)
            index = '上海' + new_contract.company.name + '(' + new_contract.sign.strftime(
                "%Y") + ')' + '-' + new_contract.subject.tag + '-' + str(
                Contract.objects.filter(subject=new_contract.subject).count() + 1).zfill(4)
            master_contract_id = request.POST.get('master', None)
            if master_contract_id:
                new_contract.master = int(master_contract_id)
                supple_count = Contract.objects.filter(master=int(master_contract_id)).count()
                index = Contract.objects.get(id=new_contract.master).index + '-补-' + str(supple_count + 1).zfill(4)
            new_contract.index = index
            new_contract.save()
            messages.success(request, '合同新增成功')
            return redirect(reverse('contracts:contract_detail', args=[new_contract.id]))
        messages.error(request, '请检查填写是否正确')
        return render(request, 'contracts/contracts_add.html', {'form': form})


@login_required
def contract_edit(request, contract_id):
    if request.method == "GET":
        contract = get_object_or_404(Contract, id=contract_id)
        form = ContractForm(instance=contract)
        return render(request, 'contracts/contracts_edit.html', {'form': form, 'contract': contract})

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
            messages.success(request, '合同信息修改成功')
            return redirect(reverse('contracts:contract_detail', args=[contract.id]))
        messages.error(request, '请检查填写是否正确')
        return render(request, 'contracts/contracts_edit.html', {'form': form, 'contract': contract})
