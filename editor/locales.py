from PySide.QtCore import QLocale

Languages = {
    0 : QLocale.Abkhazian,
    1 : QLocale.Afan,
    2 : QLocale.Afar,
    3 : QLocale.Afrikaans,
    4 : QLocale.Albanian,
    5 : QLocale.Amharic,
    6 : QLocale.Arabic,
    7 : QLocale.Armenian,
    8 : QLocale.Assamese,
    9 : QLocale.Aymara,
    10 : QLocale.Azerbaijani,
    11 : QLocale.Basque,
    12 : QLocale.Bengali,
    13 : QLocale.Bhutani,
    14 : QLocale.Bihari,
    15 : QLocale.Bislama,
    16 : QLocale.Bosnian,
    17 : QLocale.Breton,
    18 : QLocale.Bulgarian,
    19 : QLocale.Burmese,
    20 : QLocale.Byelorussian,
    21 : QLocale.Cambodian,
    22 : QLocale.Catalan,
    23 : QLocale.Chinese,
    24 : QLocale.Cornish,
    25 : QLocale.Croatian,
    26 : QLocale.Czech,
    27 : QLocale.Danish,
    28 : QLocale.Dutch,
    29 : QLocale.English,
    30 : QLocale.Estonian,
    31 : QLocale.Faroese,
    32 : QLocale.Finnish,
    33 : QLocale.French,
    34 : QLocale.Galician,
    35 : QLocale.Georgian,
    36 : QLocale.German,
    37 : QLocale.Greek,
    38 : QLocale.Greenlandic,
    39 : QLocale.Gujarati,
    40 : QLocale.Hausa,
    41 : QLocale.Hebrew,
    42 : QLocale.Hindi,
    43 : QLocale.Hungarian,
    44 : QLocale.Icelandic,
    45 : QLocale.Indonesian,
    46 : QLocale.Irish,
    47 : QLocale.Italian,
    48 : QLocale.Japanese,
    49 : QLocale.Kannada,
    50 : QLocale.Kazakh,
    51 : QLocale.Kinyarwanda,
    52 : QLocale.Kirghiz,
    53 : QLocale.Korean,
    54 : QLocale.Kurdish,
    55 : QLocale.Kurundi,
    56 : QLocale.Laothian,
    57 : QLocale.Latin,
    58 : QLocale.Latvian,
    59 : QLocale.Lingala,
    60 : QLocale.Lithuanian,
    61 : QLocale.Macedonian,
    62 : QLocale.Malagasy,
    63 : QLocale.Malay,
    64 : QLocale.Malayalam,
    65 : QLocale.Maltese,
    66 : QLocale.Manx,
    67 : QLocale.Marathi,
    68 : QLocale.Mongolian,
    69 : QLocale.Nepali,
    70 : QLocale.Norwegian,
    71 : QLocale.Occitan,
    72 : QLocale.Oriya,
    73 : QLocale.Pashto,
    74 : QLocale.Persian,
    75 : QLocale.Polish,
    76 : QLocale.Portuguese,
    77 : QLocale.Punjabi,
    78 : QLocale.RhaetoRomance,
    79 : QLocale.Romanian,
    80 : QLocale.Russian,
    81 : QLocale.Sangho,
    82 : QLocale.Serbian,
    83 : QLocale.SerboCroatian,
    84 : QLocale.Sesotho,
    85 : QLocale.Setswana,
    86 : QLocale.Shona,
    87 : QLocale.Singhalese,
    88 : QLocale.Siswati,
    89 : QLocale.Slovak,
    90 : QLocale.Slovenian,
    91 : QLocale.Somali,
    92 : QLocale.Spanish,
    93 : QLocale.Sundanese,
    94 : QLocale.Swahili,
    95 : QLocale.Swedish,
    96 : QLocale.Tagalog,
    97 : QLocale.Tajik,
    98 : QLocale.Tamil,
    99 : QLocale.Telugu,
    100 : QLocale.Thai,
    101 : QLocale.Tibetan,
    102 : QLocale.Tigrinya,
    103 : QLocale.TongaLanguage,
    104 : QLocale.Tsonga,
    105 : QLocale.Turkish,
    106 : QLocale.Ukrainian,
    107 : QLocale.Urdu,
    108 : QLocale.Uzbek,
    109 : QLocale.Vietnamese,
    110 : QLocale.Welsh,
    111 : QLocale.Xhosa,
    112 : QLocale.Yoruba,
    113 : QLocale.Zulu,
    114 : QLocale.Bosnian,
    115 : QLocale.Manx,
    116 : QLocale.Cornish,
    117 : QLocale.Akan,
    118 : QLocale.Konkani,
    119 : QLocale.Ga,
    120 : QLocale.Igbo,
    121 : QLocale.Kamba,
    122 : QLocale.Blin,
    123 : QLocale.Sidamo,
    124 : QLocale.Atsam,
    125 : QLocale.Tigre,
    126 : QLocale.Jju,
    127 : QLocale.Friulian,
    128 : QLocale.Venda,
    129 : QLocale.Ewe,
    130 : QLocale.Walamo,
    131 : QLocale.Hawaiian,
    132 : QLocale.Tyap,
    133 : QLocale.Filipino,
    134 : QLocale.SwissGerman,
    135 : QLocale.SichuanYi,
    136 : QLocale.LowGerman,
    137 : QLocale.SouthNdebele,
    138 : QLocale.NorthernSotho,
    139 : QLocale.NorthernSami,
    140 : QLocale.Taroko,
    141 : QLocale.Gusii,
    142 : QLocale.Taita,
    143 : QLocale.Fulah,
    144 : QLocale.Kikuyu,
    145 : QLocale.Samburu,
    146 : QLocale.Sena,
    147 : QLocale.NorthNdebele,
    148 : QLocale.Rombo,
    149 : QLocale.Tachelhit,
    150 : QLocale.Kabyle,
    151 : QLocale.Nyankole,
    152 : QLocale.Bena,
    153 : QLocale.Vunjo,
    154 : QLocale.Bambara,
    155 : QLocale.Embu,
    156 : QLocale.Cherokee,
    157 : QLocale.Morisyen,
    158 : QLocale.Makonde,
    159 : QLocale.Langi,
    160 : QLocale.Ganda,
    161 : QLocale.Bemba,
    162 : QLocale.Kabuverdianu,
    163 : QLocale.Meru,
    164 : QLocale.Kalenjin,
    165 : QLocale.Nama,
    166 : QLocale.Machame,
    167 : QLocale.Colognian,
    168 : QLocale.Masai,
    169 : QLocale.Soga,
    170 : QLocale.Luyia,
    171 : QLocale.Asu,
    172 : QLocale.Teso,
    173 : QLocale.Saho,
    174 : QLocale.KoyraChiini,
    175 : QLocale.Rwa,
    176 : QLocale.Luo,
    177 : QLocale.Chiga,
    178 : QLocale.CentralMoroccoTamazight,
    179 : QLocale.KoyraboroSenni,
    180 : QLocale.Shambala,
}