import json
from cost.cost_model import load, calculate, break_even

def scenarios():
    a = load()
    for field, values in {'input_tokens':[300,450,900], 'output_tokens':[80,180,360],
                          'ops_hours':[0,4,16], 'selfhost_ops_hours':[0,16,32]}.items():
        for value in values:
            changed = type(a).model_validate({**a.model_dump(),field:value})
            yield {'changed':field,'value':value,**calculate(changed),
                   'break_even_requests':break_even(changed)}

if __name__ == '__main__':
    print(json.dumps(list(scenarios()),indent=2))
