# Conservative lyric-onset alignment report

Whisper source: `out/_lyric_alignment_v01/song.json` (local, generated, not tracked).

The line windows remain authoritative. The first six hand-timed
phrases are preserved. A later phrase is eligible only when every word
matches in order inside its line window. Corrections are early-only:
detected onsets receive a 1-frame early bias, and a word
is never moved later than its existing frame.

- Line-window tolerance: ±0.45 seconds
- Minimum phrase-average lexical match: 0.88
- Minimum phrase-average confidence: 0.30
- Fully matched phrases: 40 / 87
- Eligible phrases: 40
- Changed phrases: 30
- Changed words: 80
- Median applied shift: -8 frames

| Phrase | Word | Heard | Current | Detected+bias | Applied | Shift | Match | Confidence |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `lyr-008` | me | me | 832 | 826 | 828 | -4 | 1.00 | 1.00 |
| `lyr-008` | what | what | 837 | 830 | 830 | -7 | 1.00 | 1.00 |
| `lyr-008` | you | you | 842 | 835 | 835 | -7 | 1.00 | 0.99 |
| `lyr-008` | got. | got, | 847 | 839 | 839 | -8 | 1.00 | 0.92 |
| `lyr-010` | don't | don't | 928 | 922 | 922 | -6 | 1.00 | 1.00 |
| `lyr-010` | see | see | 941 | 933 | 933 | -8 | 1.00 | 0.99 |
| `lyr-010` | anything. | anything | 953 | 939 | 939 | -14 | 1.00 | 1.00 |
| `lyr-011` | you | you | 982 | 972 | 973 | -9 | 1.00 | 1.00 |
| `lyr-011` | forgot | forgot | 991 | 981 | 981 | -10 | 1.00 | 0.99 |
| `lyr-011` | to | to | 1003 | 993 | 993 | -10 | 1.00 | 1.00 |
| `lyr-011` | attach | attach | 1011 | 1002 | 1002 | -9 | 1.00 | 1.00 |
| `lyr-011` | it. | it | 1022 | 1015 | 1015 | -7 | 1.00 | 1.00 |
| `lyr-012` | you've | you've | 1038 | 1034 | 1034 | -4 | 1.00 | 0.98 |
| `lyr-012` | got | got | 1048 | 1044 | 1044 | -4 | 1.00 | 1.00 |
| `lyr-012` | it, | it, | 1057 | 1052 | 1052 | -5 | 1.00 | 1.00 |
| `lyr-012` | give | give | 1065 | 1060 | 1060 | -5 | 1.00 | 1.00 |
| `lyr-012` | it. | it | 1074 | 1067 | 1067 | -7 | 1.00 | 1.00 |
| `lyr-014` | on | on | 1165 | 1163 | 1163 | -2 | 1.00 | 1.00 |
| `lyr-014` | it | it | 1177 | 1170 | 1170 | -7 | 1.00 | 1.00 |
| `lyr-014` | now. | now | 1188 | 1175 | 1175 | -13 | 1.00 | 1.00 |
| `lyr-015` | see | see | 1226 | 1213 | 1213 | -13 | 1.00 | 1.00 |
| `lyr-015` | what's | what's | 1240 | 1222 | 1222 | -18 | 1.00 | 0.98 |
| `lyr-015` | your | your | 1257 | 1239 | 1239 | -18 | 1.00 | 1.00 |
| `lyr-015` | deal. | deal | 1272 | 1246 | 1246 | -26 | 1.00 | 0.99 |
| `lyr-018` | the | the | 1528 | 1519 | 1519 | -9 | 1.00 | 0.99 |
| `lyr-018` | psychedelic | psychedelic | 1538 | 1524 | 1524 | -14 | 1.00 | 0.98 |
| `lyr-018` | garden. | garden | 1555 | 1553 | 1553 | -2 | 1.00 | 0.98 |
| `lyr-019` | with | with | 1588 | 1580 | 1580 | -8 | 1.00 | 0.98 |
| `lyr-019` | no | no | 1601 | 1587 | 1587 | -14 | 1.00 | 1.00 |
| `lyr-019` | name | name | 1611 | 1592 | 1592 | -19 | 1.00 | 1.00 |
| `lyr-019` | is | is | 1624 | 1605 | 1605 | -19 | 1.00 | 1.00 |
| `lyr-019` | waking | waking | 1634 | 1621 | 1621 | -13 | 1.00 | 0.84 |
| `lyr-037` | spin | spin | 2370 | 2366 | 2366 | -4 | 1.00 | 0.66 |
| `lyr-037` | your | your | 2377 | 2370 | 2370 | -7 | 1.00 | 0.99 |
| `lyr-037` | world | world | 2384 | 2374 | 2374 | -10 | 1.00 | 1.00 |
| `lyr-037` | around. | around | 2391 | 2383 | 2383 | -8 | 1.00 | 0.99 |
| `lyr-039` | it | it | 2425 | 2423 | 2423 | -2 | 1.00 | 0.99 |
| `lyr-039` | better. | better | 2430 | 2425 | 2425 | -5 | 1.00 | 0.70 |
| `lyr-040` | want | want | 2449 | 2442 | 2442 | -7 | 1.00 | 0.99 |
| `lyr-040` | fake | fake | 2461 | 2449 | 2449 | -12 | 1.00 | 0.98 |
| `lyr-040` | shit. | shit | 2473 | 2459 | 2459 | -14 | 1.00 | 0.95 |
| `lyr-041` | the | the | 2492 | 2488 | 2488 | -4 | 1.00 | 0.89 |
| `lyr-041` | thing | thing | 2499 | 2494 | 2494 | -5 | 1.00 | 0.99 |
| `lyr-041` | underneath | underneath | 2508 | 2500 | 2500 | -8 | 1.00 | 0.98 |
| `lyr-041` | it. | it | 2519 | 2514 | 2514 | -5 | 1.00 | 0.98 |
| `lyr-042` | it | it | 2538 | 2532 | 2532 | -6 | 1.00 | 0.97 |
| `lyr-042` | stupid. | stupid | 2548 | 2538 | 2538 | -10 | 1.00 | 0.87 |
| `lyr-043` | stupid. | stupid | 2599 | 2595 | 2595 | -4 | 1.00 | 1.00 |
| `lyr-045` | I | I | 2645 | 2643 | 2643 | -2 | 1.00 | 0.98 |
| `lyr-045` | meant? | meant? | 2650 | 2647 | 2647 | -3 | 1.00 | 0.94 |
| `lyr-047` | always. | always | 2723 | 2715 | 2715 | -8 | 1.00 | 1.00 |
| `lyr-048` | leaves | leaves | 2770 | 2759 | 2759 | -11 | 1.00 | 0.99 |
| `lyr-048` | thread. | threat | 2791 | 2780 | 2780 | -11 | 0.83 | 0.48 |
| `lyr-058` | bends | bends | 3576 | 3568 | 3568 | -8 | 1.00 | 0.47 |
| `lyr-058` | your | your | 3592 | 3586 | 3586 | -6 | 1.00 | 0.93 |
| `lyr-058` | mind. | mind | 3606 | 3598 | 3598 | -8 | 1.00 | 0.98 |
| `lyr-060` | the | the | 3702 | 3696 | 3696 | -6 | 1.00 | 0.99 |
| `lyr-060` | rivers | rivers | 3717 | 3707 | 3707 | -10 | 1.00 | 0.96 |
| `lyr-060` | of | of | 3737 | 3720 | 3720 | -17 | 1.00 | 0.93 |
| `lyr-060` | Mars. | Mars | 3749 | 3732 | 3732 | -17 | 1.00 | 0.86 |
| `lyr-061` | falls | falls | 3775 | 3761 | 3761 | -14 | 1.00 | 0.93 |
| `lyr-061` | from | from | 3793 | 3791 | 3791 | -2 | 1.00 | 0.53 |
| `lyr-061` | heaven | heaven | 3810 | 3807 | 3807 | -3 | 1.00 | 0.74 |
| `lyr-062` | the | the | 3848 | 3835 | 3835 | -13 | 1.00 | 0.82 |
| `lyr-062` | senses | senses | 3861 | 3840 | 3840 | -21 | 1.00 | 0.99 |
| `lyr-062` | behind. | behind | 3879 | 3854 | 3854 | -25 | 1.00 | 1.00 |
| `lyr-063` | one | one | 3899 | 3892 | 3892 | -7 | 1.00 | 0.97 |
| `lyr-063` | has | has | 3911 | 3902 | 3902 | -9 | 1.00 | 1.00 |
| `lyr-063` | ever | ever | 3923 | 3912 | 3912 | -11 | 1.00 | 1.00 |
| `lyr-063` | been | been | 3936 | 3921 | 3921 | -15 | 1.00 | 1.00 |
| `lyr-065` | turns. | turns | 4052 | 4045 | 4045 | -7 | 1.00 | 0.96 |
| `lyr-066` | follows. | follows | 4086 | 4079 | 4079 | -7 | 1.00 | 1.00 |
| `lyr-070` | mind. | mind | 4276 | 4270 | 4270 | -6 | 1.00 | 0.58 |
| `lyr-072` | on. | on | 4352 | 4350 | 4350 | -2 | 1.00 | 1.00 |
| `lyr-073` | I | I | 4373 | 4367 | 4367 | -6 | 1.00 | 1.00 |
| `lyr-073` | heard | heard | 4379 | 4371 | 4371 | -8 | 1.00 | 0.99 |
| `lyr-073` | something. | something | 4388 | 4377 | 4377 | -11 | 1.00 | 0.99 |
| `lyr-074` | did. | did | 4416 | 4407 | 4407 | -9 | 1.00 | 0.99 |
| `lyr-078` | goodnight. | goodnight | 4516 | 4511 | 4511 | -5 | 1.00 | 0.95 |
| `lyr-081` | first. | first | 4634 | 4628 | 4628 | -6 | 1.00 | 0.98 |
