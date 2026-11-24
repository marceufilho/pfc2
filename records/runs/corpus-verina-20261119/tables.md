# Tests versus proofs on ported units

| Unit | Verdict | Upstream tests | On port | On certified C | Code lines | Clause lines |
| --- | --- | ---: | --- | --- | ---: | ---: |
| verina_advanced_1 | full | 5 | pass | pass | 14 | 1 |
| verina_advanced_11 | full | 7 | pass | pass | 14 | 1 |
| verina_advanced_12 | full | 8 | pass | pass | 14 | 2 |
| verina_advanced_14 | full | 13 | pass | pass | 12 | 3 |
| verina_advanced_15 | full | 7 | pass | pass | 20 | 1 |
| verina_advanced_16 | full | 5 | pass | pass | 12 | 3 |
| verina_advanced_17 | full | 5 | pass | pass | 12 | 3 |
| verina_advanced_18 | memory | 6 | pass | pass | 24 | 2 |
| verina_advanced_19 | full | 5 | pass | pass | 38 | 5 |
| verina_advanced_20 | full | 10 | pass | pass | 15 | 2 |
| verina_advanced_21 | full | 5 | pass | pass | 12 | 5 |
| verina_advanced_22 | full | 6 | pass | pass | 15 | 3 |
| verina_advanced_23 | full | 7 | pass | pass | 12 | 2 |
| verina_advanced_28 | memory | 5 | pass | pass | 26 | 5 |
| verina_advanced_29 | full | 5 | pass | pass | 18 | 7 |
| verina_advanced_30 | full | 6 | pass | pass | 18 | 4 |
| verina_advanced_35 | full | 5 | pass | pass | 15 | 2 |
| verina_advanced_36 | full | 5 | pass | pass | 15 | 2 |
| verina_advanced_37 | full | 10 | pass | pass | 15 | 2 |
| verina_advanced_39 | full | 5 | pass | pass | 9 | 3 |
| verina_advanced_40 | full | 5 | pass | pass | 9 | 3 |
| verina_advanced_41 | full | 5 | pass | pass | 11 | 2 |
| verina_advanced_42 | memory | 5 | pass | pass | 16 | 4 |
| verina_advanced_43 | refused-failed | 5 | pass | None | 35 | 2 |
| verina_advanced_44 | memory | 8 | pass | pass | 16 | 4 |
| verina_advanced_45 | memory | 5 | pass | pass | 19 | 2 |
| verina_advanced_46 | memory | 8 | pass | pass | 14 | 2 |
| verina_advanced_49 | full | 5 | pass | pass | 24 | 7 |
| verina_advanced_5 | refused-failed | 4 | pass | None | 17 | 7 |
| verina_advanced_50 | full | 8 | pass | pass | 24 | 7 |
| verina_advanced_51 | full | 5 | pass | pass | 24 | 7 |
| verina_advanced_52 | full | 8 | pass | pass | 20 | 6 |
| verina_advanced_53 | full | 8 | pass | pass | 17 | 3 |
| verina_advanced_54 | refused-failed | 5 | pass | None | 7 | 3 |
| verina_advanced_55 | full | 5 | pass | pass | 16 | 3 |
| verina_advanced_56 | full | 9 | pass | pass | 13 | 5 |
| verina_advanced_57 | memory | 7 | pass | pass | 14 | 7 |
| verina_advanced_58 | memory | 5 | pass | pass | 28 | 4 |
| verina_advanced_59 | full | 6 | pass | pass | 36 | 3 |
| verina_advanced_6 | full | 6 | pass | pass | 24 | 3 |
| verina_advanced_61 | memory | 5 | pass | pass | 12 | 5 |
| verina_advanced_62 | refused-failed | 6 | pass | None | 25 | 4 |
| verina_advanced_63 | full | 11 | pass | pass | 12 | 4 |
| verina_advanced_64 | full | 5 | pass | pass | 10 | 5 |
| verina_advanced_65 | full | 5 | pass | pass | 6 | 6 |
| verina_advanced_66 | full | 5 | pass | pass | 22 | 8 |
| verina_advanced_68 | full | 9 | pass | pass | 24 | 7 |
| verina_advanced_69 | full | 7 | pass | pass | 13 | 5 |
| verina_advanced_7 | memory | 6 | pass | pass | 7 | 2 |
| verina_advanced_70 | memory | 5 | pass | pass | 20 | 3 |
| verina_advanced_71 | full | 9 | pass | pass | 37 | 8 |
| verina_advanced_72 | full | 7 | pass | pass | 19 | 5 |
| verina_advanced_73 | full | 5 | pass | pass | 11 | 3 |
| verina_advanced_74 | full | 5 | pass | pass | 18 | 5 |
| verina_advanced_75 | memory | 5 | pass | pass | 15 | 2 |
| verina_advanced_76 | full | 5 | pass | pass | 33 | 6 |
| verina_advanced_77 | memory | 6 | pass | pass | 21 | 4 |
| verina_advanced_78 | memory | 5 | pass | pass | 11 | 4 |
| verina_advanced_79 | memory | 5 | pass | pass | 13 | 6 |
| verina_advanced_8 | memory | 7 | pass | pass | 18 | 4 |
| verina_advanced_80 | memory | 5 | pass | pass | 11 | 7 |
| verina_advanced_81 | full | 5 | pass | pass | 17 | 6 |
| verina_advanced_9 | full | 5 | pass | pass | 14 | 5 |
| verina_basic_1 | full | 11 | pass | pass | 7 | 2 |
| verina_basic_10 | full | 7 | pass | pass | 8 | 3 |
| verina_basic_100 | memory | 5 | pass | pass | 7 | 1 |
| verina_basic_101 | memory | 5 | pass | pass | 5 | 1 |
| verina_basic_102 | memory | 7 | pass | pass | 11 | 4 |
| verina_basic_103 | memory | 5 | pass | pass | 8 | 7 |
| verina_basic_105 | memory | 5 | pass | pass | 10 | 4 |
| verina_basic_106 | memory | 5 | pass | pass | 6 | 4 |
| verina_basic_107 | refused-failed | 5 | pass | None | 4 | 1 |
| verina_basic_11 | full | 8 | pass | pass | 4 | 3 |
| verina_basic_12 | memory | 5 | pass | pass | 4 | 2 |
| verina_basic_13 | memory | 5 | pass | pass | 6 | 3 |
| verina_basic_14 | full | 9 | pass | pass | 8 | 2 |
| verina_basic_15 | memory | 8 | pass | pass | 8 | 2 |
| verina_basic_16 | refused-failed | 7 | pass | None | 10 | 3 |
| verina_basic_17 | full | 6 | pass | pass | 10 | 3 |
| verina_basic_18 | full | 6 | pass | pass | 9 | 3 |
| verina_basic_19 | full | 7 | pass | pass | 8 | 2 |
| verina_basic_2 | full | 8 | pass | pass | 15 | 4 |
| verina_basic_20 | memory | 7 | pass | pass | 15 | 4 |
| verina_basic_21 | memory | 8 | pass | pass | 11 | 7 |
| verina_basic_22 | full | 8 | pass | pass | 39 | 11 |
| verina_basic_23 | memory | 6 | pass | pass | 13 | 3 |
| verina_basic_24 | memory | 5 | pass | pass | 23 | 2 |
| verina_basic_26 | full | 5 | pass | pass | 7 | 1 |
| verina_basic_27 | full | 6 | pass | pass | 13 | 4 |
| verina_basic_28 | full | 8 | pass | pass | 8 | 3 |
| verina_basic_29 | full | 4 | pass | pass | 8 | 5 |
| verina_basic_3 | full | 12 | pass | pass | 7 | 1 |
| verina_basic_30 | refused-failed | 3 | pass | None | 14 | 5 |
| verina_basic_31 | full | 5 | pass | pass | 10 | 4 |
| verina_basic_32 | full | 4 | pass | pass | 8 | 7 |
| verina_basic_33 | full | 5 | pass | pass | 11 | 3 |
| verina_basic_34 | full | 6 | pass | pass | 10 | 4 |
| verina_basic_35 | full | 5 | pass | pass | 13 | 5 |
| verina_basic_36 | full | 4 | pass | pass | 10 | 4 |
| verina_basic_37 | full | 6 | pass | pass | 11 | 3 |
| verina_basic_38 | full | 6 | pass | pass | 8 | 3 |
| verina_basic_39 | memory | 4 | pass | pass | 10 | 5 |
| verina_basic_4 | full | 10 | pass | pass | 4 | 2 |
| verina_basic_40 | full | 6 | pass | pass | 16 | 3 |
| verina_basic_41 | full | 6 | pass | pass | 8 | 3 |
| verina_basic_42 | full | 7 | pass | pass | 9 | 3 |
| verina_basic_43 | memory | 6 | pass | pass | 8 | 3 |
| verina_basic_44 | memory | 7 | pass | pass | 8 | 2 |
| verina_basic_45 | memory | 3 | pass | pass | 24 | 1 |
| verina_basic_46 | full | 7 | pass | pass | 9 | 2 |
| verina_basic_47 | memory | 4 | pass | pass | 8 | 1 |
| verina_basic_48 | memory | 10 | pass | pass | 11 | 2 |
| verina_basic_49 | full | 6 | pass | pass | 12 | 5 |
| verina_basic_5 | memory | 7 | pass | pass | 4 | 1 |
| verina_basic_50 | memory | 5 | pass | pass | 7 | 1 |
| verina_basic_51 | full | 5 | pass | pass | 13 | 3 |
| verina_basic_52 | full | 5 | pass | pass | 15 | 2 |
| verina_basic_53 | memory | 5 | pass | pass | 7 | 3 |
| verina_basic_54 | memory | 5 | pass | pass | 23 | 4 |
| verina_basic_55 | full | 2 | pass | pass | 7 | 1 |
| verina_basic_56 | full | 5 | pass | pass | 11 | 7 |
| verina_basic_57 | full | 5 | pass | pass | 9 | 2 |
| verina_basic_58 | memory | 5 | pass | pass | 7 | 2 |
| verina_basic_59 | memory | 5 | pass | pass | 6 | 2 |
| verina_basic_6 | full | 9 | pass | pass | 11 | 2 |
| verina_basic_60 | full | 7 | pass | pass | 10 | 2 |
| verina_basic_61 | full | 5 | pass | pass | 9 | 1 |
| verina_basic_62 | full | 5 | pass | pass | 9 | 1 |
| verina_basic_64 | full | 5 | pass | pass | 14 | 5 |
| verina_basic_65 | memory | 5 | pass | pass | 7 | 3 |
| verina_basic_66 | full | 5 | pass | pass | 7 | 1 |
| verina_basic_68 | full | 5 | pass | pass | 9 | 3 |
| verina_basic_69 | full | 5 | pass | pass | 7 | 4 |
| verina_basic_7 | memory | 7 | pass | pass | 4 | 2 |
| verina_basic_71 | full | 5 | pass | pass | 9 | 5 |
| verina_basic_72 | full | 5 | pass | pass | 8 | 4 |
| verina_basic_73 | full | 5 | pass | pass | 12 | 2 |
| verina_basic_74 | full | 5 | pass | pass | 10 | 1 |
| verina_basic_75 | full | 5 | pass | pass | 10 | 1 |
| verina_basic_76 | full | 5 | pass | pass | 7 | 2 |
| verina_basic_78 | memory | 5 | pass | pass | 6 | 2 |
| verina_basic_79 | full | 7 | pass | pass | 18 | 6 |
| verina_basic_8 | full | 8 | pass | pass | 7 | 2 |
| verina_basic_81 | full | 5 | pass | pass | 11 | 5 |
| verina_basic_82 | full | 5 | pass | pass | 7 | 3 |
| verina_basic_83 | full | 5 | pass | pass | 10 | 3 |
| verina_basic_84 | full | 5 | pass | pass | 11 | 2 |
| verina_basic_85 | full | 5 | pass | pass | 7 | 2 |
| verina_basic_86 | memory | 6 | pass | pass | 7 | 3 |
| verina_basic_87 | full | 5 | pass | pass | 17 | 3 |
| verina_basic_88 | full | 5 | pass | pass | 7 | 2 |
| verina_basic_89 | full | 5 | pass | pass | 17 | 2 |
| verina_basic_9 | full | 8 | pass | pass | 11 | 2 |
| verina_basic_91 | full | 5 | pass | pass | 6 | 3 |
| verina_basic_92 | full | 5 | pass | pass | 6 | 3 |
| verina_basic_93 | full | 5 | pass | pass | 6 | 3 |
| verina_basic_94 | full | 5 | pass | pass | 7 | 2 |
| verina_basic_95 | full | 5 | pass | pass | 9 | 6 |
| verina_basic_96 | full | 5 | pass | pass | 6 | 3 |
| verina_basic_97 | full | 5 | pass | pass | 8 | 4 |
| verina_basic_98 | memory | 5 | pass | pass | 4 | 1 |
| verina_basic_99 | memory | 5 | pass | pass | 4 | 1 |

Upstream assertions restated as laws over the contract alone.

| Unit | Assertions | Subsumed | Not subsumed | Not expressible | Not judged or error |
| --- | ---: | ---: | ---: | ---: | ---: |
| verina_advanced_1 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_11 | 7 | 0 | 7 | 0 | 0 |
| verina_advanced_12 | 8 | 0 | 8 | 0 | 0 |
| verina_advanced_14 | 13 | 0 | 13 | 0 | 0 |
| verina_advanced_15 | 7 | 0 | 7 | 0 | 0 |
| verina_advanced_16 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_17 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_18 | 6 | 0 | 6 | 0 | 0 |
| verina_advanced_19 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_20 | 10 | 4 | 6 | 0 | 0 |
| verina_advanced_21 | 5 | 2 | 3 | 0 | 0 |
| verina_advanced_22 | 6 | 0 | 6 | 0 | 0 |
| verina_advanced_23 | 7 | 0 | 7 | 0 | 0 |
| verina_advanced_28 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_29 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_30 | 6 | 1 | 5 | 0 | 0 |
| verina_advanced_35 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_36 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_37 | 10 | 0 | 10 | 0 | 0 |
| verina_advanced_39 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_40 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_41 | 5 | 5 | 0 | 0 | 0 |
| verina_advanced_42 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_44 | 8 | 2 | 6 | 0 | 0 |
| verina_advanced_45 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_46 | 8 | 0 | 8 | 0 | 0 |
| verina_advanced_49 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_50 | 8 | 1 | 7 | 0 | 0 |
| verina_advanced_51 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_52 | 8 | 0 | 8 | 0 | 0 |
| verina_advanced_53 | 8 | 1 | 7 | 0 | 0 |
| verina_advanced_55 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_56 | 9 | 1 | 8 | 0 | 0 |
| verina_advanced_57 | 7 | 0 | 7 | 0 | 0 |
| verina_advanced_58 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_59 | 6 | 0 | 6 | 0 | 0 |
| verina_advanced_6 | 6 | 0 | 6 | 0 | 0 |
| verina_advanced_61 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_63 | 11 | 2 | 9 | 0 | 0 |
| verina_advanced_64 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_65 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_66 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_68 | 9 | 1 | 8 | 0 | 0 |
| verina_advanced_69 | 7 | 0 | 7 | 0 | 0 |
| verina_advanced_7 | 6 | 0 | 6 | 0 | 0 |
| verina_advanced_70 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_71 | 9 | 0 | 9 | 0 | 0 |
| verina_advanced_72 | 7 | 0 | 7 | 0 | 0 |
| verina_advanced_73 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_74 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_75 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_76 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_77 | 6 | 0 | 6 | 0 | 0 |
| verina_advanced_78 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_79 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_8 | 7 | 0 | 7 | 0 | 0 |
| verina_advanced_80 | 5 | 0 | 5 | 0 | 0 |
| verina_advanced_81 | 5 | 1 | 4 | 0 | 0 |
| verina_advanced_9 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_1 | 11 | 11 | 0 | 0 | 0 |
| verina_basic_10 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_100 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_101 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_102 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_103 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_105 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_106 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_11 | 8 | 8 | 0 | 0 | 0 |
| verina_basic_12 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_13 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_14 | 9 | 0 | 9 | 0 | 0 |
| verina_basic_15 | 8 | 0 | 8 | 0 | 0 |
| verina_basic_17 | 6 | 1 | 5 | 0 | 0 |
| verina_basic_18 | 6 | 0 | 6 | 0 | 0 |
| verina_basic_19 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_2 | 8 | 0 | 8 | 0 | 0 |
| verina_basic_20 | 7 | 1 | 6 | 0 | 0 |
| verina_basic_21 | 8 | 3 | 5 | 0 | 0 |
| verina_basic_22 | 8 | 0 | 8 | 0 | 0 |
| verina_basic_23 | 6 | 0 | 6 | 0 | 0 |
| verina_basic_24 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_26 | 5 | 5 | 0 | 0 | 0 |
| verina_basic_27 | 6 | 0 | 6 | 0 | 0 |
| verina_basic_28 | 8 | 0 | 8 | 0 | 0 |
| verina_basic_29 | 4 | 1 | 3 | 0 | 0 |
| verina_basic_3 | 12 | 12 | 0 | 0 | 0 |
| verina_basic_31 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_32 | 4 | 0 | 4 | 0 | 0 |
| verina_basic_33 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_34 | 6 | 1 | 5 | 0 | 0 |
| verina_basic_35 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_36 | 4 | 1 | 3 | 0 | 0 |
| verina_basic_37 | 6 | 3 | 3 | 0 | 0 |
| verina_basic_38 | 6 | 1 | 5 | 0 | 0 |
| verina_basic_39 | 4 | 1 | 3 | 0 | 0 |
| verina_basic_4 | 10 | 10 | 0 | 0 | 0 |
| verina_basic_40 | 6 | 0 | 6 | 0 | 0 |
| verina_basic_41 | 6 | 0 | 6 | 0 | 0 |
| verina_basic_42 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_43 | 6 | 0 | 6 | 0 | 0 |
| verina_basic_44 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_45 | 3 | 0 | 3 | 0 | 0 |
| verina_basic_46 | 7 | 2 | 5 | 0 | 0 |
| verina_basic_47 | 4 | 0 | 4 | 0 | 0 |
| verina_basic_48 | 10 | 0 | 10 | 0 | 0 |
| verina_basic_49 | 6 | 0 | 6 | 0 | 0 |
| verina_basic_5 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_50 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_51 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_52 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_53 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_54 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_55 | 2 | 2 | 0 | 0 | 0 |
| verina_basic_56 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_57 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_58 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_59 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_6 | 9 | 9 | 0 | 0 | 0 |
| verina_basic_60 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_61 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_62 | 5 | 2 | 3 | 0 | 0 |
| verina_basic_64 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_65 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_66 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_68 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_69 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_7 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_71 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_72 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_73 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_74 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_75 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_76 | 5 | 5 | 0 | 0 | 0 |
| verina_basic_78 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_79 | 7 | 0 | 7 | 0 | 0 |
| verina_basic_8 | 8 | 8 | 0 | 0 | 0 |
| verina_basic_81 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_82 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_83 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_84 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_85 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_86 | 6 | 1 | 5 | 0 | 0 |
| verina_basic_87 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_88 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_89 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_9 | 8 | 0 | 8 | 0 | 0 |
| verina_basic_91 | 5 | 5 | 0 | 0 | 0 |
| verina_basic_92 | 5 | 5 | 0 | 0 | 0 |
| verina_basic_93 | 5 | 5 | 0 | 0 | 0 |
| verina_basic_94 | 5 | 1 | 4 | 0 | 0 |
| verina_basic_95 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_96 | 5 | 5 | 0 | 0 | 0 |
| verina_basic_97 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_98 | 5 | 0 | 5 | 0 | 0 |
| verina_basic_99 | 5 | 0 | 5 | 0 | 0 |

Mutants: tests kill / proof refuses with a failed obligation.

| Unit | Mutants | Both | Tests only | Proof only | Neither | Proof inconclusive | Rejected by front end |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| verina_advanced_1 | 10 | 1 | 6 | 2 | 1 | 0 | 0 |
| verina_advanced_11 | 14 | 2 | 7 | 2 | 3 | 0 | 0 |
| verina_advanced_12 | 19 | 8 | 6 | 1 | 4 | 0 | 0 |
| verina_advanced_14 | 14 | 4 | 9 | 0 | 1 | 0 | 0 |
| verina_advanced_15 | 22 | 2 | 9 | 1 | 10 | 0 | 0 |
| verina_advanced_16 | 9 | 3 | 5 | 1 | 0 | 0 | 0 |
| verina_advanced_17 | 9 | 3 | 5 | 1 | 0 | 0 | 0 |
| verina_advanced_18 | 34 | 1 | 29 | 0 | 4 | 0 | 0 |
| verina_advanced_19 | 28 | 4 | 20 | 1 | 3 | 0 | 0 |
| verina_advanced_20 | 25 | 9 | 14 | 0 | 2 | 0 | 0 |
| verina_advanced_21 | 10 | 10 | 0 | 0 | 0 | 0 | 0 |
| verina_advanced_22 | 14 | 2 | 7 | 0 | 5 | 0 | 0 |
| verina_advanced_23 | 14 | 4 | 9 | 1 | 0 | 0 | 0 |
| verina_advanced_28 | 20 | 2 | 12 | 2 | 4 | 0 | 0 |
| verina_advanced_29 | 17 | 4 | 9 | 3 | 1 | 0 | 0 |
| verina_advanced_30 | 19 | 9 | 7 | 1 | 2 | 0 | 0 |
| verina_advanced_35 | 11 | 3 | 3 | 1 | 4 | 0 | 0 |
| verina_advanced_36 | 11 | 2 | 5 | 2 | 2 | 0 | 0 |
| verina_advanced_37 | 11 | 3 | 6 | 1 | 1 | 0 | 0 |
| verina_advanced_39 | 4 | 3 | 0 | 0 | 1 | 0 | 0 |
| verina_advanced_40 | 4 | 3 | 0 | 0 | 1 | 0 | 0 |
| verina_advanced_41 | 6 | 3 | 0 | 1 | 2 | 0 | 0 |
| verina_advanced_42 | 13 | 7 | 3 | 1 | 2 | 0 | 0 |
| verina_advanced_44 | 18 | 9 | 7 | 0 | 2 | 0 | 0 |
| verina_advanced_45 | 17 | 4 | 7 | 2 | 4 | 0 | 0 |
| verina_advanced_46 | 11 | 1 | 7 | 0 | 3 | 0 | 0 |
| verina_advanced_49 | 16 | 10 | 5 | 0 | 1 | 0 | 0 |
| verina_advanced_50 | 16 | 10 | 5 | 0 | 1 | 0 | 0 |
| verina_advanced_51 | 16 | 10 | 5 | 0 | 1 | 0 | 0 |
| verina_advanced_52 | 15 | 3 | 8 | 0 | 4 | 0 | 0 |
| verina_advanced_53 | 28 | 12 | 13 | 1 | 2 | 0 | 0 |
| verina_advanced_55 | 9 | 0 | 6 | 1 | 2 | 0 | 0 |
| verina_advanced_56 | 8 | 2 | 6 | 0 | 0 | 0 | 0 |
| verina_advanced_57 | 8 | 1 | 6 | 0 | 1 | 0 | 0 |
| verina_advanced_58 | 34 | 2 | 30 | 1 | 1 | 0 | 0 |
| verina_advanced_59 | 32 | 3 | 21 | 0 | 8 | 0 | 0 |
| verina_advanced_6 | 33 | 1 | 21 | 0 | 11 | 0 | 0 |
| verina_advanced_61 | 8 | 0 | 8 | 0 | 0 | 0 | 0 |
| verina_advanced_63 | 10 | 7 | 3 | 0 | 0 | 0 | 0 |
| verina_advanced_64 | 4 | 1 | 3 | 0 | 0 | 0 | 0 |
| verina_advanced_65 | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| verina_advanced_66 | 16 | 6 | 8 | 0 | 2 | 0 | 0 |
| verina_advanced_68 | 22 | 4 | 13 | 0 | 5 | 7 | 1 |
| verina_advanced_69 | 13 | 12 | 0 | 0 | 1 | 0 | 0 |
| verina_advanced_7 | 6 | 0 | 6 | 0 | 0 | 0 | 0 |
| verina_advanced_70 | 19 | 3 | 11 | 3 | 2 | 0 | 0 |
| verina_advanced_71 | 35 | 11 | 16 | 1 | 7 | 0 | 0 |
| verina_advanced_72 | 32 | 27 | 0 | 5 | 0 | 0 | 0 |
| verina_advanced_73 | 5 | 1 | 2 | 0 | 2 | 0 | 0 |
| verina_advanced_74 | 10 | 2 | 7 | 0 | 1 | 0 | 0 |
| verina_advanced_75 | 11 | 2 | 7 | 0 | 2 | 0 | 0 |
| verina_advanced_76 | 22 | 2 | 16 | 2 | 2 | 0 | 0 |
| verina_advanced_77 | 13 | 4 | 6 | 0 | 3 | 0 | 0 |
| verina_advanced_78 | 9 | 1 | 6 | 0 | 2 | 0 | 0 |
| verina_advanced_79 | 17 | 14 | 1 | 0 | 2 | 0 | 0 |
| verina_advanced_8 | 21 | 14 | 7 | 0 | 0 | 0 | 0 |
| verina_advanced_80 | 10 | 9 | 0 | 1 | 0 | 0 | 0 |
| verina_advanced_81 | 12 | 4 | 6 | 0 | 2 | 0 | 0 |
| verina_advanced_9 | 13 | 5 | 8 | 0 | 0 | 0 | 0 |
| verina_basic_1 | 15 | 15 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_10 | 5 | 1 | 3 | 0 | 1 | 0 | 0 |
| verina_basic_100 | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_101 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_102 | 9 | 1 | 6 | 0 | 2 | 0 | 0 |
| verina_basic_103 | 14 | 13 | 1 | 0 | 0 | 0 | 0 |
| verina_basic_105 | 6 | 0 | 3 | 0 | 3 | 0 | 0 |
| verina_basic_106 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| verina_basic_11 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_12 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_13 | 3 | 0 | 3 | 0 | 0 | 0 | 0 |
| verina_basic_14 | 5 | 1 | 4 | 0 | 0 | 0 | 0 |
| verina_basic_15 | 10 | 3 | 7 | 0 | 0 | 0 | 0 |
| verina_basic_17 | 7 | 1 | 5 | 0 | 1 | 0 | 0 |
| verina_basic_18 | 8 | 4 | 4 | 0 | 0 | 0 | 0 |
| verina_basic_19 | 8 | 3 | 5 | 0 | 0 | 0 | 0 |
| verina_basic_2 | 18 | 12 | 3 | 0 | 3 | 0 | 0 |
| verina_basic_20 | 8 | 2 | 5 | 0 | 1 | 0 | 0 |
| verina_basic_21 | 6 | 5 | 1 | 0 | 0 | 0 | 0 |
| verina_basic_22 | 27 | 5 | 14 | 3 | 5 | 0 | 0 |
| verina_basic_23 | 9 | 3 | 4 | 0 | 2 | 0 | 0 |
| verina_basic_24 | 18 | 0 | 14 | 0 | 4 | 0 | 0 |
| verina_basic_26 | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_27 | 17 | 7 | 4 | 1 | 5 | 0 | 0 |
| verina_basic_28 | 6 | 1 | 5 | 0 | 0 | 0 | 0 |
| verina_basic_29 | 8 | 6 | 2 | 0 | 0 | 0 | 0 |
| verina_basic_3 | 8 | 8 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_31 | 7 | 1 | 5 | 0 | 1 | 0 | 0 |
| verina_basic_32 | 11 | 10 | 1 | 0 | 0 | 0 | 0 |
| verina_basic_33 | 5 | 1 | 2 | 0 | 2 | 0 | 0 |
| verina_basic_34 | 8 | 1 | 7 | 0 | 0 | 0 | 0 |
| verina_basic_35 | 8 | 2 | 6 | 0 | 0 | 0 | 0 |
| verina_basic_36 | 5 | 0 | 5 | 0 | 0 | 0 | 0 |
| verina_basic_37 | 6 | 4 | 1 | 0 | 1 | 0 | 0 |
| verina_basic_38 | 5 | 2 | 2 | 0 | 1 | 0 | 0 |
| verina_basic_39 | 6 | 5 | 1 | 0 | 0 | 0 | 0 |
| verina_basic_4 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_40 | 14 | 0 | 6 | 0 | 8 | 0 | 0 |
| verina_basic_41 | 5 | 1 | 3 | 0 | 1 | 0 | 0 |
| verina_basic_42 | 6 | 1 | 5 | 0 | 0 | 0 | 0 |
| verina_basic_43 | 11 | 11 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_44 | 8 | 1 | 7 | 0 | 0 | 0 | 0 |
| verina_basic_45 | 21 | 0 | 13 | 1 | 7 | 0 | 0 |
| verina_basic_46 | 10 | 7 | 3 | 0 | 0 | 0 | 0 |
| verina_basic_47 | 5 | 1 | 3 | 0 | 1 | 0 | 0 |
| verina_basic_48 | 10 | 1 | 9 | 0 | 0 | 0 | 0 |
| verina_basic_49 | 21 | 12 | 4 | 1 | 4 | 0 | 0 |
| verina_basic_5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_50 | 4 | 2 | 0 | 0 | 2 | 0 | 0 |
| verina_basic_51 | 13 | 10 | 2 | 0 | 1 | 0 | 0 |
| verina_basic_52 | 20 | 7 | 9 | 3 | 1 | 0 | 0 |
| verina_basic_53 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_54 | 21 | 5 | 5 | 1 | 10 | 0 | 0 |
| verina_basic_55 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_56 | 10 | 4 | 4 | 0 | 2 | 0 | 0 |
| verina_basic_57 | 4 | 1 | 3 | 0 | 0 | 0 | 0 |
| verina_basic_58 | 7 | 1 | 5 | 1 | 0 | 0 | 0 |
| verina_basic_59 | 12 | 11 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_6 | 6 | 4 | 0 | 0 | 2 | 0 | 0 |
| verina_basic_60 | 8 | 1 | 7 | 0 | 0 | 0 | 0 |
| verina_basic_61 | 10 | 2 | 5 | 1 | 2 | 0 | 0 |
| verina_basic_62 | 7 | 5 | 1 | 1 | 0 | 0 | 0 |
| verina_basic_64 | 14 | 6 | 5 | 0 | 3 | 0 | 0 |
| verina_basic_65 | 2 | 1 | 1 | 0 | 0 | 0 | 0 |
| verina_basic_66 | 8 | 1 | 7 | 0 | 0 | 0 | 0 |
| verina_basic_68 | 4 | 2 | 1 | 0 | 1 | 0 | 0 |
| verina_basic_69 | 2 | 1 | 1 | 0 | 0 | 0 | 0 |
| verina_basic_7 | 17 | 17 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_71 | 3 | 1 | 2 | 0 | 0 | 0 | 0 |
| verina_basic_72 | 8 | 5 | 2 | 0 | 1 | 0 | 0 |
| verina_basic_73 | 10 | 2 | 5 | 1 | 2 | 0 | 0 |
| verina_basic_74 | 8 | 2 | 2 | 0 | 4 | 0 | 0 |
| verina_basic_75 | 8 | 2 | 3 | 0 | 3 | 0 | 0 |
| verina_basic_76 | 2 | 1 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_78 | 8 | 7 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_79 | 20 | 10 | 6 | 0 | 4 | 0 | 0 |
| verina_basic_8 | 2 | 1 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_81 | 17 | 15 | 0 | 0 | 2 | 0 | 0 |
| verina_basic_82 | 11 | 8 | 2 | 0 | 1 | 0 | 0 |
| verina_basic_83 | 10 | 4 | 4 | 0 | 2 | 0 | 0 |
| verina_basic_84 | 9 | 1 | 7 | 1 | 0 | 0 | 0 |
| verina_basic_85 | 8 | 5 | 2 | 1 | 0 | 0 | 0 |
| verina_basic_86 | 6 | 3 | 2 | 1 | 0 | 0 | 0 |
| verina_basic_87 | 12 | 1 | 7 | 3 | 1 | 0 | 0 |
| verina_basic_88 | 4 | 1 | 2 | 1 | 0 | 0 | 0 |
| verina_basic_89 | 13 | 1 | 9 | 0 | 3 | 0 | 0 |
| verina_basic_9 | 10 | 3 | 5 | 0 | 2 | 0 | 0 |
| verina_basic_91 | 6 | 5 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_92 | 6 | 5 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_93 | 6 | 5 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_94 | 4 | 1 | 2 | 1 | 0 | 0 | 0 |
| verina_basic_95 | 6 | 3 | 2 | 0 | 1 | 0 | 0 |
| verina_basic_96 | 6 | 5 | 0 | 0 | 1 | 0 | 0 |
| verina_basic_97 | 7 | 4 | 2 | 0 | 1 | 0 | 0 |
| verina_basic_98 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| verina_basic_99 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
