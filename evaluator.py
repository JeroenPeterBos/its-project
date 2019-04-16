import pandas
from fractions import Fraction as f
from statistics import Ensamble
from compression import Arithmetic, BossArithmetic

columns = [
    'EntropyEx',
    'MessageEx',
    'MessageLengthEx',
    'MinimalLengthEx',
    'StandardEncoding',
    'StandardEncodingLength',
    'StandardDecodingMatchOnLength',
    'EntropyInc',
    'MessageInc',
    'MessageLengthInc',
    'MinimalLengthInc',
    'StandardEncodingInc',
    'StandardEncodingIncLength',
    'StandardDecodingMatchOnEOF',
    'BossEncoding',
    'BossEncodingLength',
    'BossDecodingMatch'
]

ensambles = [
    ('ab_1_10', Ensamble(['a','b'],[f(1,10),f(9,10)])),
    ('ab_2_10', Ensamble(['a','b'],[f(2,10),f(8,10)])),
    ('ab_3_10', Ensamble(['a','b'],[f(3,10),f(7,10)])),
    ('ab_4_10', Ensamble(['a','b'],[f(4,10),f(6,10)])),
    ('ab_5_10', Ensamble(['a','b'],[f(5,10),f(5,10)])),
    ('abc_1_1_10', Ensamble(['a','b','c'],[f(1,10),f(1,10),f(8,10)])),
    ('abc_1_2_10', Ensamble(['a','b','c'],[f(1,10),f(2,10),f(7,10)])),
    ('abc_1_3_10', Ensamble(['a','b','c'],[f(1,10),f(3,10),f(6,10)])),
    ('abc_1_4_10', Ensamble(['a','b','c'],[f(1,10),f(4,10),f(5,10)])),
    ('abc_2_2_10', Ensamble(['a','b','c'],[f(2,10),f(2,10),f(6,10)])),
    ('abc_2_3_10', Ensamble(['a','b','c'],[f(2,10),f(3,10),f(5,10)])),
    ('abc_2_4_10', Ensamble(['a','b','c'],[f(2,10),f(4,10),f(4,10)])),
    ('abc_3_3_10', Ensamble(['a','b','c'],[f(3,10),f(3,10),f(4,10)])),
]

lengths = list(range(3,10))

all_df = pandas.DataFrame(columns=columns)
for name, ensamble in ensambles:
    df = pandas.DataFrame(columns=columns)
    for l in lengths:
        messages = ensamble.A()
        for x in range(l-1):
            new_messages = []
            for message in messages:
                for a in ensamble.A():
                    new_messages.append(message + a)
            messages = new_messages
        
        ensamble2 = ensamble.copy()
        ensamble2.expand('.', f(1,l))

        standard_ar = Arithmetic(ensamble)
        standard_ar_inc = Arithmetic(ensamble2)
        boss_ar = BossArithmetic(ensamble2)

        for message in messages:
            print("Ensamble: {:<10} Message: {:<15}".format(name,message))
            standard_enc = standard_ar.encode(message)
            standard_dec = standard_ar.decode(standard_enc, len(message))
            
            standard_enc_inc = standard_ar_inc.encode(message + '.')
            standard_dec_eof = standard_ar_inc.decode(standard_enc_inc)

            boss_enc = boss_ar.encode(message + '.')
            boss_dec = boss_ar.decode(boss_enc)
            
            row = [
                ensamble.entropy(),
                message,
                len(message),
                ensamble.min_encoding_length(message),
                standard_enc,
                len(standard_enc),
                1 if standard_dec == message else 0,
                ensamble2.entropy(),
                message + '.',
                len(message + '.'),
                ensamble2.min_encoding_length(message + '.'),
                standard_enc_inc,
                len(standard_enc_inc),
                1 if standard_dec_eof == message + '.' else 0,
                boss_enc,
                len(boss_enc),
                1 if boss_dec == message + '.' else 0
            ]
            df.loc[len(df.index)] = row
            all_df.loc[len(all_df.index)] = row
        df.to_csv('output/{}.csv'.format(name))
        all_df.to_csv('output/all.csv')

        