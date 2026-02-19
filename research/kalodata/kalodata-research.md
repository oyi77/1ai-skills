# KALODATA RESEARCH-STEP.md
---------------------------------------------

1. buka https://www.kalodata.com/product
2. lakukan filtering dengan cara : 
```fetch("https://www.kalodata.com/product/queryList", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "country": "ID",
    "currency": "IDR",
    "language": "id-ID",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"144.0.7559.133\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Google Chrome\";v=\"144.0.7559.133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.1.703409481.1763715310; _fbp=fb.1.1763715310221.187697897347332450; _bl_uid=Ugm29iCt8d6m1jkO13n95b7o896q; AGL_USER_ID=aab5a9c2-b63c-45a9-8823-55634afcf381; appVersion=2.0; deviceType=pc; deviceId=68d71b733cd37e9b5aa79c4e966834a2; _tt_enable_cookie=1; _ttp=01KAJSZVA7EGV7RWKP92XEXRTZ_.tt.1; _c_WBKFRo=gDYIP2YPWhPnrWEF5bbG30q8KsRzALNy74Hyre77; Hm_lvt_8aa1693861618ac63989ae373e684811=1766854733; smidV2=20260107181141fa0cb2637b725506b6eb378daa4d0ce1002f3d6a56996bc10; _gcl_au=1.1.596047495.1763715310.1541373569.1768299173.1768299173; _clck=x55t8z%5E2%5Eg2o%5E0%5E2151; _uetvid=c905e330c6b711f09e5b55ffe8b88d71; ttcsid=1768313627416::TMWHNSmi-ZLwyTqkPiEg.20.1768313639075.0; ttcsid_CM9SHDBC77U4KJBR96OG=1768313627416::LZ1BgEuWf68QXRTty_YQ.20.1768313639075.0; _ga_Q21FRKKG88=GS2.1.s1768314042$o25$g1$t1768314397$j60$l0$h0; page_session=ef77b014-bb30-4000-9138-f4dd0f2c733e; SESSION=NzZiYTYwNzktYTc5MC00NDZlLTk1NjQtZDViMGQyMTZiYjI0; _cfuvid=GQpw3nDdCEdxpc0HXn7.UWWC.kKR95RmiAiwGbHYtoc-1771473802.513278-1.0.1.1-IErZBqs0Nu0V8ZlKwsD.tQx3QA1rKuxcAo47AeCUTn0; cf_clearance=QThg05rfWChRF6RvVaFmazmA6xFMBk90UhMh.W2vjwI-1771473803-1.2.1.1-SN8VQ4sHtxbQICHiK7hJpbsC8KFwd8wJgNngg6qQJMVMSfO.YEjayJYwSWYEvcie0Ed4.c7dQjUg.8qb079LxbVZY4EWpFRwbHosPKZLWSw0YJwncYpYSMccfQkIKvpQ3sSQS2a.IC9TZbk82DGD.MF8h9hN62ioFqnKm0PWDiKg6ZyjZtHq9HDOp4UxVLSVciwYReE2JvRTWcORKYYCyJ91gowMAjywIuRiRdfrnVA; .thumbcache_211a882976e013454a0403b9c1967076=L/O07PpH3ROZfQuMOJ7Z3202Q70/znE3EjJMUqg1cv0X9EhGCmXRwyn5jKcJkCI93T5bfxq9oPAdfWjNwlB2YA%3D%3D",
    "Referer": "https://www.kalodata.com/product"
  },
  "body": "{\"country\":\"ID\",\"startDate\":\"2026-01-20\",\"endDate\":\"2026-02-18\",\"cateIds\":[\"601152\"],\"showCateIds\":[\"601152\"],\"pageNo\":1,\"pageSize\":10,\"sort\":[{\"field\":\"revenue\",\"type\":\"DESC\"}],\"product.filter.sales_channel\":[\"VIDEO\"],\"product.filter.strategy\":\"INDEPENDENT\",\"product.filter.unit_price\":\">20000\",\"product.filter.affiliate_type\":\"PUBLIC_PLAN\",\"product.filter.creator\":\"10-100\"}",
  "method": "POST"
});
```

### dapatkan response :
```
{
    "success": true,
    "data": [
        {
            "sec_cate_id": 842760,
            "is_full_service": 0,
            "ter_cate_id": 601291,
            "is_overseas": 0,
            "gmv_A": 4349593.755722344,
            "creator_conversion_ratio": 0.37037037037037035,
            "unit_price": "Rp156,48RB",
            "gmv_B": 245477.90078973962,
            "product_title": "Raya One set Setelan Wanita Premium Rayon Model Baru",
            "is_tokopedia": 0,
            "revenue": "Rp778,83JT",
            "sale": 4977,
            "creator_num": 81,
            "revenue_trend": [
                81770.0,
                98013.0,
                89197.0,
                110001.0,
                132230.0,
                95752.0,
                106426.0,
                112891.0,
                195943.0,
                100797.0,
                183760.0,
                197124.0,
                209795.0,
                218835.0,
                148461.0,
                152823.0,
                411668.0,
                567177.0,
                399917.0,
                383910.0,
                403007.0,
                316458.0,
                324148.0,
                317548.0,
                303235.0,
                421494.0,
                342393.0,
                315765.0,
                434572.0,
                310239.0
            ],
            "min_real_price": "Rp162,16RB",
            "delivery_type": "local",
            "revenue_grouping_rate": ">999.9%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp162,16RB",
            "commission_rate": "2%",
            "id": "1732844308471449032",
            "launch_date": "2025-10-20",
            "product_rating": 4.7
        },
        {
            "sec_cate_id": 842248,
            "is_full_service": 0,
            "ter_cate_id": 843400,
            "is_overseas": 0,
            "gmv_A": 1154569.2732724093,
            "creator_conversion_ratio": 0.5052631578947369,
            "unit_price": "Rp32,79RB",
            "gmv_B": 1878267.428499919,
            "product_title": "Blazer Outer Crop Kancing 1 Terbaru Scuba Wanita Atasan Baju Basic Panjang jaket crop korean style Lembut Oversize Linen Cardigan",
            "is_tokopedia": 0,
            "revenue": "Rp514,04JT",
            "sale": 15677,
            "creator_num": 95,
            "revenue_trend": [
                112313.0,
                88516.0,
                101894.0,
                116628.0,
                374739.0,
                110789.0,
                119179.0,
                64822.0,
                69542.0,
                87945.0,
                145933.0,
                149053.0,
                112550.0,
                112097.0,
                121938.0,
                85428.0,
                74928.0,
                171221.0,
                114654.0,
                74443.0,
                59775.0,
                47784.0,
                50042.0,
                70736.0,
                62740.0,
                170262.0,
                60703.0,
                49469.0,
                50211.0,
                53130.0
            ],
            "min_real_price": "Rp58,55RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "-38.5%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp111,46RB",
            "commission_rate": "10%",
            "id": "1730004337700932599",
            "launch_date": "2024-02-18",
            "product_rating": 4.8
        },
        {
            "sec_cate_id": 842376,
            "is_full_service": 0,
            "ter_cate_id": 601277,
            "is_overseas": 0,
            "gmv_A": 1648026.9193238062,
            "creator_conversion_ratio": 0.676923076923077,
            "unit_price": "Rp55,18RB",
            "gmv_B": 1145782.546962291,
            "product_title": "CASSANDRA PANTS CELANA SCUBA SUPER JUMBO",
            "is_tokopedia": 0,
            "revenue": "Rp473,53JT",
            "sale": 8582,
            "creator_num": 65,
            "revenue_trend": [
                65557.0,
                69870.0,
                51328.0,
                52670.0,
                76576.0,
                72698.0,
                62008.0,
                63848.0,
                104197.0,
                65868.0,
                107339.0,
                99294.0,
                104927.0,
                92759.0,
                121964.0,
                161775.0,
                123040.0,
                113253.0,
                95297.0,
                91743.0,
                107742.0,
                107794.0,
                115917.0,
                125905.0,
                131716.0,
                106420.0,
                84104.0,
                108456.0,
                96417.0,
                109010.0
            ],
            "min_real_price": "Rp61,14RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "43.8%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp85,60RB",
            "commission_rate": "9%",
            "id": "1729890526743529777",
            "launch_date": "2024-02-28",
            "product_rating": 4.8
        },
        {
            "sec_cate_id": 842504,
            "is_full_service": 0,
            "ter_cate_id": 601281,
            "is_overseas": 0,
            "gmv_A": 2191259.8475537226,
            "creator_conversion_ratio": 0.26666666666666666,
            "unit_price": "Rp209,98RB",
            "gmv_B": 326116.7086965071,
            "product_title": "Kanaya Gamis Dress Bahan Sabrina Anti Uv Lembut Bahan Jatuh - Bestiie Fashion",
            "is_tokopedia": 0,
            "revenue": "Rp426,67JT",
            "sale": 2032,
            "creator_num": 15,
            "revenue_trend": [
                4981.0,
                1462.0,
                0.0,
                1274.0,
                0.0,
                0.0,
                0.0,
                125706.0,
                289790.0,
                60943.0,
                78764.0,
                120847.0,
                201166.0,
                165991.0,
                184072.0,
                61810.0,
                92125.0,
                223555.0,
                261783.0,
                551372.0,
                505168.0,
                433769.0,
                309773.0,
                317605.0,
                281161.0,
                223284.0,
                186809.0,
                266005.0,
                170934.0,
                147202.0
            ],
            "min_real_price": "Rp205,39RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "571.9%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp216,80RB",
            "commission_rate": "10%",
            "id": "1733835297396327762",
            "launch_date": "2026-01-03",
            "product_rating": 4.8
        },
        {
            "sec_cate_id": 842760,
            "is_full_service": 0,
            "ter_cate_id": 601291,
            "is_overseas": 0,
            "gmv_A": 725725.9040194331,
            "creator_conversion_ratio": 0.5555555555555556,
            "unit_price": "Rp242,08RB",
            "gmv_B": 1775229.9031326617,
            "product_title": "FADFAD Setelan dua potong tanpa lengan dengan atasan modis dan rok motif cetak bunga",
            "is_tokopedia": 0,
            "revenue": "Rp423,89JT",
            "sale": 1751,
            "creator_num": 18,
            "revenue_trend": [
                53012.0,
                50564.0,
                79360.0,
                85535.0,
                91858.0,
                137353.0,
                117495.0,
                73800.0,
                141089.0,
                221806.0,
                146401.0,
                161653.0,
                112179.0,
                191128.0,
                113439.0,
                104768.0,
                85195.0,
                89510.0,
                70923.0,
                59820.0,
                68192.0,
                40126.0,
                24515.0,
                35272.0,
                13969.0,
                34379.0,
                38676.0,
                28740.0,
                9939.0,
                21700.0
            ],
            "min_real_price": "Rp244,25RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "-59.1%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp246,71RB",
            "commission_rate": "5%",
            "id": "1732107720546879234",
            "launch_date": "2025-08-06",
            "product_rating": 4.8
        },
        {
            "sec_cate_id": 842376,
            "is_full_service": 0,
            "ter_cate_id": 601276,
            "is_overseas": 0,
            "gmv_A": 1304964.0676710182,
            "creator_conversion_ratio": 0.2857142857142857,
            "unit_price": "Rp350,65RB",
            "gmv_B": 896249.7337169851,
            "product_title": "YEONA - DUNE JEANS | Straight Jeans",
            "is_tokopedia": 0,
            "revenue": "Rp373,09JT",
            "sale": 1064,
            "creator_num": 91,
            "revenue_trend": [
                72133.0,
                100350.0,
                84538.0,
                100771.0,
                95107.0,
                109174.0,
                112238.0,
                87337.0,
                65605.0,
                97110.0,
                100345.0,
                70062.0,
                90880.0,
                133816.0,
                76904.0,
                99038.0,
                84569.0,
                137779.0,
                91585.0,
                96335.0,
                94667.0,
                76584.0,
                83174.0,
                109614.0,
                147366.0,
                124533.0,
                132110.0,
                114268.0,
                119196.0,
                125879.0
            ],
            "min_real_price": "Rp360,21RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "45.6%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp440,78RB",
            "commission_rate": "3%",
            "id": "1731599515393164672",
            "launch_date": "2025-06-12",
            "product_rating": 4.9
        },
        {
            "sec_cate_id": 842376,
            "is_full_service": 0,
            "ter_cate_id": 601277,
            "is_overseas": 0,
            "gmv_A": 689045.0558872586,
            "creator_conversion_ratio": 0.578125,
            "unit_price": "Rp85,49RB",
            "gmv_B": 1389068.1241024258,
            "product_title": "Livie Pants - Highwaist Celana Wanita - Celana Panjang lipetan - Celana Kasual- Celana wanita Fashion Muslim -",
            "is_tokopedia": 0,
            "revenue": "Rp352,22JT",
            "sale": 4120,
            "creator_num": 64,
            "revenue_trend": [
                72046.0,
                57861.0,
                52661.0,
                60625.0,
                66531.0,
                71910.0,
                72217.0,
                78715.0,
                131623.0,
                122541.0,
                294966.0,
                337512.0,
                209849.0,
                232620.0,
                209821.0,
                195597.0,
                178205.0,
                104476.0,
                95358.0,
                51530.0,
                44611.0,
                33896.0,
                26370.0,
                20233.0,
                17334.0,
                10089.0,
                10990.0,
                9629.0,
                8577.0,
                5112.0
            ],
            "min_real_price": "Rp107,88RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "-50.4%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp112,42RB",
            "commission_rate": "10%",
            "id": "1733989685298628228",
            "launch_date": "2026-01-14",
            "product_rating": 4.8
        },
        {
            "sec_cate_id": 842888,
            "is_full_service": 0,
            "ter_cate_id": 601262,
            "is_overseas": 0,
            "gmv_A": 892195.842820619,
            "creator_conversion_ratio": 0.7142857142857143,
            "unit_price": "Rp40,82RB",
            "gmv_B": 1055903.414647102,
            "product_title": "3 PC Bra Wanita Seamless Ringan Bra Tanpa Kawat Motif Renda Anti Gatal bRA kATUN IBu Menyusui Bh Bumil Kancing Depan Busui",
            "is_tokopedia": 0,
            "revenue": "Rp330,19JT",
            "sale": 8088,
            "creator_num": 91,
            "revenue_trend": [
                4404.0,
                12062.0,
                11208.0,
                7426.0,
                14498.0,
                27274.0,
                30690.0,
                44674.0,
                112980.0,
                132615.0,
                196587.0,
                149990.0,
                124017.0,
                122571.0,
                85174.0,
                107829.0,
                69120.0,
                78477.0,
                77120.0,
                69105.0,
                74423.0,
                56021.0,
                73784.0,
                53090.0,
                50705.0,
                57958.0,
                51721.0,
                46822.0,
                42114.0,
                57009.0
            ],
            "min_real_price": "Rp104,05RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "-15.5%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp104,05RB",
            "commission_rate": "11%",
            "id": "1730787152125986560",
            "launch_date": "2025-04-29",
            "product_rating": 4.6
        },
        {
            "sec_cate_id": 842888,
            "is_full_service": 0,
            "ter_cate_id": 601262,
            "is_overseas": 0,
            "gmv_A": 983018.1700131133,
            "creator_conversion_ratio": 0.5238095238095238,
            "unit_price": "Rp134,88RB",
            "gmv_B": 840901.6926974144,
            "product_title": "GRENEY-2pcs Bra Cup Coconut 3D-Mengumpulkan tanpa bekas  Penopang  Tanpa kawat  Nyaman  Cup 3D  Mencegah Lipatan Nakal  Mencegah kekenduran-89981",
            "is_tokopedia": 1,
            "revenue": "Rp309,14JT",
            "sale": 2292,
            "creator_num": 84,
            "revenue_trend": [
                127340.0,
                104311.0,
                70220.0,
                99384.0,
                88860.0,
                132490.0,
                122820.0,
                122084.0,
                191509.0,
                65538.0,
                156258.0,
                94709.0,
                112922.0,
                166771.0,
                134762.0,
                146229.0,
                118860.0,
                131791.0,
                126873.0,
                116723.0,
                116180.0,
                129566.0,
                123640.0,
                135060.0,
                112577.0,
                119058.0,
                117606.0,
                119159.0,
                151485.0,
                141266.0
            ],
            "min_real_price": "Rp217,46RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "16.9%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp217,46RB",
            "commission_rate": "8%",
            "id": "1731764929989347216",
            "launch_date": "2025-06-29",
            "product_rating": 4.9
        },
        {
            "sec_cate_id": 842376,
            "is_full_service": 0,
            "ter_cate_id": 601277,
            "is_overseas": 0,
            "gmv_A": 701904.3555072098,
            "creator_conversion_ratio": 0.4444444444444444,
            "unit_price": "Rp66,44RB",
            "gmv_B": 1118163.9185034567,
            "product_title": "Alika Cullote Pants Semiwool Celana Kulot Kantor Formal Wanita Premium Bahan Semiwool Tidak Melar",
            "is_tokopedia": 0,
            "revenue": "Rp308,49JT",
            "sale": 4643,
            "creator_num": 45,
            "revenue_trend": [
                35980.0,
                47777.0,
                48337.0,
                151033.0,
                76340.0,
                46429.0,
                42425.0,
                58663.0,
                53515.0,
                74409.0,
                189851.0,
                117228.0,
                107367.0,
                128373.0,
                90037.0,
                76653.0,
                114481.0,
                76222.0,
                66442.0,
                49222.0,
                60393.0,
                48706.0,
                46109.0,
                34575.0,
                30610.0,
                25266.0,
                14200.0,
                18450.0,
                18392.0,
                22184.0
            ],
            "min_real_price": "Rp85,12RB",
            "delivery_type": "local",
            "revenue_grouping_rate": "-37.2%",
            "pri_cate_id": 601152,
            "max_real_price": "Rp97,62RB",
            "commission_rate": "10%",
            "id": "1733939920522479441",
            "launch_date": "2026-01-12",
            "product_rating": 4.7
        }
    ],
    "message": null,
    "cached": null,
    "code": null
}
```
3. Dapatkan data video : 
```
fetch("https://www.kalodata.com/product/enrich", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "country": "ID",
    "currency": "IDR",
    "language": "id-ID",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"144.0.7559.133\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Google Chrome\";v=\"144.0.7559.133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.1.703409481.1763715310; _fbp=fb.1.1763715310221.187697897347332450; _bl_uid=Ugm29iCt8d6m1jkO13n95b7o896q; AGL_USER_ID=aab5a9c2-b63c-45a9-8823-55634afcf381; appVersion=2.0; deviceType=pc; deviceId=68d71b733cd37e9b5aa79c4e966834a2; _tt_enable_cookie=1; _ttp=01KAJSZVA7EGV7RWKP92XEXRTZ_.tt.1; _c_WBKFRo=gDYIP2YPWhPnrWEF5bbG30q8KsRzALNy74Hyre77; Hm_lvt_8aa1693861618ac63989ae373e684811=1766854733; smidV2=20260107181141fa0cb2637b725506b6eb378daa4d0ce1002f3d6a56996bc10; _gcl_au=1.1.596047495.1763715310.1541373569.1768299173.1768299173; _clck=x55t8z%5E2%5Eg2o%5E0%5E2151; _uetvid=c905e330c6b711f09e5b55ffe8b88d71; ttcsid=1768313627416::TMWHNSmi-ZLwyTqkPiEg.20.1768313639075.0; ttcsid_CM9SHDBC77U4KJBR96OG=1768313627416::LZ1BgEuWf68QXRTty_YQ.20.1768313639075.0; _ga_Q21FRKKG88=GS2.1.s1768314042$o25$g1$t1768314397$j60$l0$h0; page_session=ef77b014-bb30-4000-9138-f4dd0f2c733e; SESSION=NzZiYTYwNzktYTc5MC00NDZlLTk1NjQtZDViMGQyMTZiYjI0; _cfuvid=GQpw3nDdCEdxpc0HXn7.UWWC.kKR95RmiAiwGbHYtoc-1771473802.513278-1.0.1.1-IErZBqs0Nu0V8ZlKwsD.tQx3QA1rKuxcAo47AeCUTn0; cf_clearance=QThg05rfWChRF6RvVaFmazmA6xFMBk90UhMh.W2vjwI-1771473803-1.2.1.1-SN8VQ4sHtxbQICHiK7hJpbsC8KFwd8wJgNngg6qQJMVMSfO.YEjayJYwSWYEvcie0Ed4.c7dQjUg.8qb079LxbVZY4EWpFRwbHosPKZLWSw0YJwncYpYSMccfQkIKvpQ3sSQS2a.IC9TZbk82DGD.MF8h9hN62ioFqnKm0PWDiKg6ZyjZtHq9HDOp4UxVLSVciwYReE2JvRTWcORKYYCyJ91gowMAjywIuRiRdfrnVA; .thumbcache_211a882976e013454a0403b9c1967076=L/O07PpH3ROZfQuMOJ7Z3202Q70/znE3EjJMUqg1cv0X9EhGCmXRwyn5jKcJkCI93T5bfxq9oPAdfWjNwlB2YA%3D%3D",
    "Referer": "https://www.kalodata.com/product"
  },
  "body": "{\"ids\":[\"1732844308471449032\",\"1730004337700932599\",\"1729890526743529777\",\"1733835297396327762\",\"1732107720546879234\",\"1731599515393164672\",\"1733989685298628228\",\"1730787152125986560\",\"1731764929989347216\",\"1733939920522479441\"],\"country\":\"ID\",\"startDate\":\"2026-01-20\",\"endDate\":\"2026-02-18\",\"cateIds\":[\"601152\"]}",
  "method": "POST"
});
```
### Response : 
```
{
    "success": true,
    "data": [
        {
            "id": "1732844308471449032",
            "videos": [
                {
                    "id": "7600772739623914770",
                    "contentType": "video"
                },
                {
                    "id": "7601457368899030279",
                    "contentType": "video"
                },
                {
                    "id": "7585188716826742037",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1730004337700932599",
            "videos": [
                {
                    "id": "7588148736656706823",
                    "contentType": "video"
                },
                {
                    "id": "7581810890840739090",
                    "contentType": "video"
                },
                {
                    "id": "7592077729764330760",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1729890526743529777",
            "videos": [
                {
                    "id": "7597817446690688274",
                    "contentType": "video"
                },
                {
                    "id": "7598353765686660370",
                    "contentType": "video"
                },
                {
                    "id": "7567633616038022408",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1733835297396327762",
            "videos": [
                {
                    "id": "7594864024861330709",
                    "contentType": "video"
                },
                {
                    "id": "7598813125944610069",
                    "contentType": "video"
                },
                {
                    "id": "7602986398408264968",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1732107720546879234",
            "videos": [
                {
                    "id": "7587754757414997269",
                    "contentType": "video"
                },
                {
                    "id": "7587400352136318229",
                    "contentType": "video"
                },
                {
                    "id": "7581096033229294869",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1731599515393164672",
            "videos": [
                {
                    "id": "7580302949352672533",
                    "contentType": "video"
                },
                {
                    "id": "7538499666451746053",
                    "contentType": "video"
                },
                {
                    "id": "7588446763728620807",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1733989685298628228",
            "videos": [
                {
                    "id": "7595362679653502226",
                    "contentType": "video"
                },
                {
                    "id": "7594999684335258887",
                    "contentType": "video"
                },
                {
                    "id": "7595534964930694418",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1730787152125986560",
            "videos": [
                {
                    "id": "7596861567673699605",
                    "contentType": "video"
                },
                {
                    "id": "7586611522449837333",
                    "contentType": "video"
                },
                {
                    "id": "7600288180436339989",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1731764929989347216",
            "videos": [
                {
                    "id": "7573688513976110357",
                    "contentType": "autocut"
                },
                {
                    "id": "7568162426705808661",
                    "contentType": "autocut"
                },
                {
                    "id": "7547028979031575815",
                    "contentType": "video"
                }
            ]
        },
        {
            "id": "1733939920522479441",
            "videos": [
                {
                    "id": "7594491477678476564",
                    "contentType": "video"
                },
                {
                    "id": "7594387264608718100",
                    "contentType": "video"
                },
                {
                    "id": "7594430572257119506",
                    "contentType": "video"
                }
            ]
        }
    ],
    "message": null,
    "cached": true,
    "code": null
}
```
4. cek penggunaan AI : 
```
fetch("https://www.kalodata.com/benefit/checkAiUse?id=7600772739623914770&type=videoScript", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "country": "ID",
    "currency": "IDR",
    "language": "id-ID",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"144.0.7559.133\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Google Chrome\";v=\"144.0.7559.133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.1.703409481.1763715310; _fbp=fb.1.1763715310221.187697897347332450; _bl_uid=Ugm29iCt8d6m1jkO13n95b7o896q; AGL_USER_ID=aab5a9c2-b63c-45a9-8823-55634afcf381; appVersion=2.0; deviceType=pc; deviceId=68d71b733cd37e9b5aa79c4e966834a2; _tt_enable_cookie=1; _ttp=01KAJSZVA7EGV7RWKP92XEXRTZ_.tt.1; _c_WBKFRo=gDYIP2YPWhPnrWEF5bbG30q8KsRzALNy74Hyre77; Hm_lvt_8aa1693861618ac63989ae373e684811=1766854733; smidV2=20260107181141fa0cb2637b725506b6eb378daa4d0ce1002f3d6a56996bc10; _gcl_au=1.1.596047495.1763715310.1541373569.1768299173.1768299173; _clck=x55t8z%5E2%5Eg2o%5E0%5E2151; _uetvid=c905e330c6b711f09e5b55ffe8b88d71; ttcsid=1768313627416::TMWHNSmi-ZLwyTqkPiEg.20.1768313639075.0; ttcsid_CM9SHDBC77U4KJBR96OG=1768313627416::LZ1BgEuWf68QXRTty_YQ.20.1768313639075.0; _ga_Q21FRKKG88=GS2.1.s1768314042$o25$g1$t1768314397$j60$l0$h0; page_session=ef77b014-bb30-4000-9138-f4dd0f2c733e; SESSION=NzZiYTYwNzktYTc5MC00NDZlLTk1NjQtZDViMGQyMTZiYjI0; _cfuvid=GQpw3nDdCEdxpc0HXn7.UWWC.kKR95RmiAiwGbHYtoc-1771473802.513278-1.0.1.1-IErZBqs0Nu0V8ZlKwsD.tQx3QA1rKuxcAo47AeCUTn0; cf_clearance=QThg05rfWChRF6RvVaFmazmA6xFMBk90UhMh.W2vjwI-1771473803-1.2.1.1-SN8VQ4sHtxbQICHiK7hJpbsC8KFwd8wJgNngg6qQJMVMSfO.YEjayJYwSWYEvcie0Ed4.c7dQjUg.8qb079LxbVZY4EWpFRwbHosPKZLWSw0YJwncYpYSMccfQkIKvpQ3sSQS2a.IC9TZbk82DGD.MF8h9hN62ioFqnKm0PWDiKg6ZyjZtHq9HDOp4UxVLSVciwYReE2JvRTWcORKYYCyJ91gowMAjywIuRiRdfrnVA; .thumbcache_211a882976e013454a0403b9c1967076=L/O07PpH3ROZfQuMOJ7Z3202Q70/znE3EjJMUqg1cv0X9EhGCmXRwyn5jKcJkCI93T5bfxq9oPAdfWjNwlB2YA%3D%3D",
    "Referer": "https://www.kalodata.com/product"
  },
  "body": null,
  "method": "GET"
});
```
### Response :
```
{
    "success": true,
    "data": {
        "used": false,
        "progressInfo": {
            "total": 14000,
            "used": 400,
            "remain": 13600,
            "full": false
        }
    },
    "message": null,
    "cached": null,
    "code": null
}
```
5. Dapatkan Url Video : 
```
fetch("https://www.kalodata.com/video/detail/getVideoUrl?videoId=7600772739623914770", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "country": "ID",
    "currency": "IDR",
    "language": "id-ID",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"144.0.7559.133\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Google Chrome\";v=\"144.0.7559.133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.1.703409481.1763715310; _fbp=fb.1.1763715310221.187697897347332450; _bl_uid=Ugm29iCt8d6m1jkO13n95b7o896q; AGL_USER_ID=aab5a9c2-b63c-45a9-8823-55634afcf381; appVersion=2.0; deviceType=pc; deviceId=68d71b733cd37e9b5aa79c4e966834a2; _tt_enable_cookie=1; _ttp=01KAJSZVA7EGV7RWKP92XEXRTZ_.tt.1; _c_WBKFRo=gDYIP2YPWhPnrWEF5bbG30q8KsRzALNy74Hyre77; Hm_lvt_8aa1693861618ac63989ae373e684811=1766854733; smidV2=20260107181141fa0cb2637b725506b6eb378daa4d0ce1002f3d6a56996bc10; _gcl_au=1.1.596047495.1763715310.1541373569.1768299173.1768299173; _clck=x55t8z%5E2%5Eg2o%5E0%5E2151; _uetvid=c905e330c6b711f09e5b55ffe8b88d71; ttcsid=1768313627416::TMWHNSmi-ZLwyTqkPiEg.20.1768313639075.0; ttcsid_CM9SHDBC77U4KJBR96OG=1768313627416::LZ1BgEuWf68QXRTty_YQ.20.1768313639075.0; _ga_Q21FRKKG88=GS2.1.s1768314042$o25$g1$t1768314397$j60$l0$h0; page_session=ef77b014-bb30-4000-9138-f4dd0f2c733e; SESSION=NzZiYTYwNzktYTc5MC00NDZlLTk1NjQtZDViMGQyMTZiYjI0; _cfuvid=GQpw3nDdCEdxpc0HXn7.UWWC.kKR95RmiAiwGbHYtoc-1771473802.513278-1.0.1.1-IErZBqs0Nu0V8ZlKwsD.tQx3QA1rKuxcAo47AeCUTn0; cf_clearance=QThg05rfWChRF6RvVaFmazmA6xFMBk90UhMh.W2vjwI-1771473803-1.2.1.1-SN8VQ4sHtxbQICHiK7hJpbsC8KFwd8wJgNngg6qQJMVMSfO.YEjayJYwSWYEvcie0Ed4.c7dQjUg.8qb079LxbVZY4EWpFRwbHosPKZLWSw0YJwncYpYSMccfQkIKvpQ3sSQS2a.IC9TZbk82DGD.MF8h9hN62ioFqnKm0PWDiKg6ZyjZtHq9HDOp4UxVLSVciwYReE2JvRTWcORKYYCyJ91gowMAjywIuRiRdfrnVA; .thumbcache_211a882976e013454a0403b9c1967076=L/O07PpH3ROZfQuMOJ7Z3202Q70/znE3EjJMUqg1cv0X9EhGCmXRwyn5jKcJkCI93T5bfxq9oPAdfWjNwlB2YA%3D%3D",
    "Referer": "https://www.kalodata.com/product"
  },
  "body": null,
  "method": "GET"
});
```
### Response :
```
{
    "success": true,
    "data": {
        "url": "https://live.kalocdn.com/video/7600772739623914770.mp4?key=9d84799748444467a9bfeb88053f2226&time=1771474270187"
    },
    "message": null,
    "cached": null,
    "code": null
}
```

6. Ekspor script STOryboard untuk video : 
```
fetch("https://www.kalodata.com/aiTask/startAiTask", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "country": "ID",
    "currency": "IDR",
    "language": "id-ID",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"144.0.7559.133\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Google Chrome\";v=\"144.0.7559.133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.1.703409481.1763715310; _fbp=fb.1.1763715310221.187697897347332450; _bl_uid=Ugm29iCt8d6m1jkO13n95b7o896q; AGL_USER_ID=aab5a9c2-b63c-45a9-8823-55634afcf381; appVersion=2.0; deviceType=pc; deviceId=68d71b733cd37e9b5aa79c4e966834a2; _tt_enable_cookie=1; _ttp=01KAJSZVA7EGV7RWKP92XEXRTZ_.tt.1; _c_WBKFRo=gDYIP2YPWhPnrWEF5bbG30q8KsRzALNy74Hyre77; Hm_lvt_8aa1693861618ac63989ae373e684811=1766854733; smidV2=20260107181141fa0cb2637b725506b6eb378daa4d0ce1002f3d6a56996bc10; _gcl_au=1.1.596047495.1763715310.1541373569.1768299173.1768299173; _clck=x55t8z%5E2%5Eg2o%5E0%5E2151; _uetvid=c905e330c6b711f09e5b55ffe8b88d71; ttcsid=1768313627416::TMWHNSmi-ZLwyTqkPiEg.20.1768313639075.0; ttcsid_CM9SHDBC77U4KJBR96OG=1768313627416::LZ1BgEuWf68QXRTty_YQ.20.1768313639075.0; _ga_Q21FRKKG88=GS2.1.s1768314042$o25$g1$t1768314397$j60$l0$h0; page_session=ef77b014-bb30-4000-9138-f4dd0f2c733e; SESSION=NzZiYTYwNzktYTc5MC00NDZlLTk1NjQtZDViMGQyMTZiYjI0; _cfuvid=GQpw3nDdCEdxpc0HXn7.UWWC.kKR95RmiAiwGbHYtoc-1771473802.513278-1.0.1.1-IErZBqs0Nu0V8ZlKwsD.tQx3QA1rKuxcAo47AeCUTn0; PHPSESSID=26d04c8454d9d01a80554594c87866af; cf_clearance=OJHE4pWRaLjbqzcn58rKHn.YZym.fA_YPZDjG6iGpMg-1771474751-1.2.1.1-ukZ85vKFVvLmOr_Y99eSLuQzJiWyKgQWDu6ZtuGuKgDWuG91B4DetiDGT9UnJ8N_IH0c2KxJWawYmA5W6eAj6qlYOm8gEN4MD_XKs0e5k8BnSnLZH9e78EF_A0MT8HwghLFm_BoQpqpYIUmndEpgoO7AzmBOj1VZ_qmNzc29EGNNYT7XvrZfzqowGA0svqQcuX213cxkDwd8akVvrTMalxM8gyv3XgCGtzGGs884xvc; .thumbcache_211a882976e013454a0403b9c1967076=Xwxd+tBDBHUNRCV8fyKuMg0iv3HI4anO6trDBmloGi/I2VsHGBk83F7qjaTGei0UCvzGuLg5R0gO4Jnn9eRypQ%3D%3D",
    "Referer": "https://www.kalodata.com/aiStudio/script-export?id=7600772739623914770&dateRange=%5B%222026-01-20%22%2C%222026-02-18%22%5D&region=ID"
  },
  "body": "{\"id\":\"7600772739623914770\",\"type\":\"video_script\",\"partitionDayStart\":\"2026-01-20\",\"partitionDayEnd\":\"2026-02-18\",\"uuid\":\"972e192078894\"}",
  "method": "POST"
});
```

### RESPONSE PROSES : 
```
{"success":true,"data":{"code":1},"message":null,"cached":null,"code":null}
```

### RESPONSE SELESAI : 
```
{"success":true,"data":{"code":2},"message":null,"cached":null,"code":null}
```

7. Dapatkan storyboard nya : 
```
fetch("https://www.kalodata.com/aiTask/video/getVideoScript", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "country": "ID",
    "currency": "IDR",
    "language": "id-ID",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"144.0.7559.133\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Google Chrome\";v=\"144.0.7559.133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.1.703409481.1763715310; _fbp=fb.1.1763715310221.187697897347332450; _bl_uid=Ugm29iCt8d6m1jkO13n95b7o896q; AGL_USER_ID=aab5a9c2-b63c-45a9-8823-55634afcf381; appVersion=2.0; deviceType=pc; deviceId=68d71b733cd37e9b5aa79c4e966834a2; _tt_enable_cookie=1; _ttp=01KAJSZVA7EGV7RWKP92XEXRTZ_.tt.1; _c_WBKFRo=gDYIP2YPWhPnrWEF5bbG30q8KsRzALNy74Hyre77; Hm_lvt_8aa1693861618ac63989ae373e684811=1766854733; smidV2=20260107181141fa0cb2637b725506b6eb378daa4d0ce1002f3d6a56996bc10; _gcl_au=1.1.596047495.1763715310.1541373569.1768299173.1768299173; _clck=x55t8z%5E2%5Eg2o%5E0%5E2151; _uetvid=c905e330c6b711f09e5b55ffe8b88d71; ttcsid=1768313627416::TMWHNSmi-ZLwyTqkPiEg.20.1768313639075.0; ttcsid_CM9SHDBC77U4KJBR96OG=1768313627416::LZ1BgEuWf68QXRTty_YQ.20.1768313639075.0; _ga_Q21FRKKG88=GS2.1.s1768314042$o25$g1$t1768314397$j60$l0$h0; page_session=ef77b014-bb30-4000-9138-f4dd0f2c733e; SESSION=NzZiYTYwNzktYTc5MC00NDZlLTk1NjQtZDViMGQyMTZiYjI0; _cfuvid=GQpw3nDdCEdxpc0HXn7.UWWC.kKR95RmiAiwGbHYtoc-1771473802.513278-1.0.1.1-IErZBqs0Nu0V8ZlKwsD.tQx3QA1rKuxcAo47AeCUTn0; PHPSESSID=26d04c8454d9d01a80554594c87866af; cf_clearance=OJHE4pWRaLjbqzcn58rKHn.YZym.fA_YPZDjG6iGpMg-1771474751-1.2.1.1-ukZ85vKFVvLmOr_Y99eSLuQzJiWyKgQWDu6ZtuGuKgDWuG91B4DetiDGT9UnJ8N_IH0c2KxJWawYmA5W6eAj6qlYOm8gEN4MD_XKs0e5k8BnSnLZH9e78EF_A0MT8HwghLFm_BoQpqpYIUmndEpgoO7AzmBOj1VZ_qmNzc29EGNNYT7XvrZfzqowGA0svqQcuX213cxkDwd8akVvrTMalxM8gyv3XgCGtzGGs884xvc; .thumbcache_211a882976e013454a0403b9c1967076=Xwxd+tBDBHUNRCV8fyKuMg0iv3HI4anO6trDBmloGi/I2VsHGBk83F7qjaTGei0UCvzGuLg5R0gO4Jnn9eRypQ%3D%3D",
    "Referer": "https://www.kalodata.com/aiStudio/script-export?id=7600772739623914770&dateRange=%5B%222026-01-20%22%2C%222026-02-18%22%5D&region=ID"
  },
  "body": "{\"id\":\"7600772739623914770\",\"partitionDayStart\":\"2026-01-20\",\"partitionDayEnd\":\"2026-02-18\",\"translate\":false}",
  "method": "POST"
});
```
### RESPONSE : 
```
{
    "success": true,
    "data": {
        "gender": "female",
        "translate_gender": null,
        "language": "Indonesian",
        "language_code": "id-ID",
        "translate_language": null,
        "camera_work": "Video ini menggunakan teknik pengambilan gambar statis yang terfokus pada model. Terdapat sedikit pergeseran atau zoom kecil untuk menyoroti detail pakaian atau pose model. Pencahayaan terlihat merata dan alami, yang membantu menonjolkan warna cerah dan motif bunga pada pakaian. Gerakan model yang dinamis juga menjadi elemen penting untuk menunjukkan fleksibilitas dan kenyamanan pakaian saat dikenakan.",
        "translate_camera_work": null,
        "key_to_success": "1. Menampilkan setelan pakaian modis dan tertutup (modest fashion) yang sangat relevan dengan target pasar di Indonesia.2. Model secara aktif berpose dan berputar, efektif menunjukkan bagaimana pakaian terlihat dan bergerak dari berbagai sudut, membantu calon pembeli memvisualisasikan produk.3. Branding 'FashionByDea' terlihat jelas, membantu membangun pengenalan merek.4. Penggunaan musik yang ceria dan pose model yang ramah menciptakan suasana positif dan menarik, meningkatkan pengalaman menonton dan daya tarik produk.5. Video berdurasi singkat dan padat, cocok untuk format TikTok, langsung pada inti demonstrasi produk tanpa bertele-tele.",
        "key_to_success_list": [
            "1. Menampilkan setelan pakaian modis dan tertutup (modest fashion) yang sangat relevan dengan target pasar di Indonesia.2. Model secara aktif berpose dan berputar, efektif menunjukkan bagaimana pakaian terlihat dan bergerak dari berbagai sudut, membantu calon pembeli memvisualisasikan produk.3. Branding 'FashionByDea' terlihat jelas, membantu membangun pengenalan merek.4. Penggunaan musik yang ceria dan pose model yang ramah menciptakan suasana positif dan menarik, meningkatkan pengalaman menonton dan daya tarik produk.5. Video berdurasi singkat dan padat, cocok untuk format TikTok, langsung pada inti demonstrasi produk tanpa bertele-tele."
        ],
        "translate_key_to_success": null,
        "translate_key_to_success_list": null,
        "video_scripts": [
            {
                "scene": "Product Information",
                "translate_scene": null,
                "start_time": 0,
                "end_time": 2,
                "shot_scale": "Full Shot",
                "translate_shot_scale": null,
                "visual_description": "Seorang wanita berhijab mengenakan setelan tunik dan celana panjang bermotif bunga-bunga cerah. Ia berdiri di depan cermin dan dinding berpanel kayu, tersenyum ke arah kamera sambil memegang ujung celana dan sedikit merapikan hijabnya.",
                "translate_visual_description": null,
                "audio_script": []
            },
            {
                "scene": "Product Selling Points",
                "translate_scene": null,
                "start_time": 2,
                "end_time": 5,
                "shot_scale": "Full Shot",
                "translate_shot_scale": null,
                "visual_description": "Wanita itu berputar perlahan untuk menunjukkan detail bagian belakang setelannya, kemudian kembali menghadap kamera, tersenyum dan merapikan pakaiannya, menonjolkan potongan dan motif dari segala sisi.",
                "translate_visual_description": null,
                "audio_script": []
            },
            {
                "scene": "Real Experience",
                "translate_scene": null,
                "start_time": 5,
                "end_time": 8,
                "shot_scale": "Full Shot",
                "translate_shot_scale": null,
                "visual_description": "Wanita itu berpose dengan tangan terkatup di depan dada, lalu memindahkan tangannya ke pinggul sambil tersenyum ceria, menunjukkan kenyamanan dan gaya setelan tersebut melalui ekspresi tubuh dan wajahnya yang bahagia.",
                "translate_visual_description": null,
                "audio_script": []
            },
            {
                "scene": "Usage Scenarios",
                "translate_scene": null,
                "start_time": 8,
                "end_time": 10,
                "shot_scale": "Full Shot",
                "translate_shot_scale": null,
                "visual_description": "Wanita berputar lagi, memperlihatkan bagaimana bahan setelan itu jatuh dan bergerak saat dipakai. Ia lalu membuat gerakan seolah-olah mengayunkan celananya, menonjolkan fitur produk seperti kelenturan kain dan desain yang longgar.",
                "translate_visual_description": null,
                "audio_script": []
            },
            {
                "scene": "Call to Action",
                "translate_scene": null,
                "start_time": 10,
                "end_time": 13,
                "shot_scale": "Full Shot",
                "translate_shot_scale": null,
                "visual_description": "Wanita itu tersenyum dan membuat gerakan tangan berbentuk hati di depan dadanya sebagai penutup video, mengundang interaksi positif dan menunjukkan apresiasi terhadap penonton.",
                "translate_visual_description": null,
                "audio_script": []
            }
        ]
    },
    "message": null,
    "cached": null,
    "code": null
}
```

8. Dapatkan total product count : 
```
fetch("https://www.kalodata.com/product/count", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "country": "ID",
    "currency": "IDR",
    "language": "id-ID",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"144.0.7559.133\"",
    "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Google Chrome\";v=\"144.0.7559.133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"19.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "_ga=GA1.1.703409481.1763715310; _fbp=fb.1.1763715310221.187697897347332450; _bl_uid=Ugm29iCt8d6m1jkO13n95b7o896q; AGL_USER_ID=aab5a9c2-b63c-45a9-8823-55634afcf381; appVersion=2.0; deviceType=pc; deviceId=68d71b733cd37e9b5aa79c4e966834a2; _tt_enable_cookie=1; _ttp=01KAJSZVA7EGV7RWKP92XEXRTZ_.tt.1; _c_WBKFRo=gDYIP2YPWhPnrWEF5bbG30q8KsRzALNy74Hyre77; Hm_lvt_8aa1693861618ac63989ae373e684811=1766854733; smidV2=20260107181141fa0cb2637b725506b6eb378daa4d0ce1002f3d6a56996bc10; _gcl_au=1.1.596047495.1763715310.1541373569.1768299173.1768299173; _clck=x55t8z%5E2%5Eg2o%5E0%5E2151; _uetvid=c905e330c6b711f09e5b55ffe8b88d71; ttcsid=1768313627416::TMWHNSmi-ZLwyTqkPiEg.20.1768313639075.0; ttcsid_CM9SHDBC77U4KJBR96OG=1768313627416::LZ1BgEuWf68QXRTty_YQ.20.1768313639075.0; _ga_Q21FRKKG88=GS2.1.s1768314042$o25$g1$t1768314397$j60$l0$h0; page_session=ef77b014-bb30-4000-9138-f4dd0f2c733e; SESSION=NzZiYTYwNzktYTc5MC00NDZlLTk1NjQtZDViMGQyMTZiYjI0; _cfuvid=GQpw3nDdCEdxpc0HXn7.UWWC.kKR95RmiAiwGbHYtoc-1771473802.513278-1.0.1.1-IErZBqs0Nu0V8ZlKwsD.tQx3QA1rKuxcAo47AeCUTn0; PHPSESSID=26d04c8454d9d01a80554594c87866af; cf_clearance=OJHE4pWRaLjbqzcn58rKHn.YZym.fA_YPZDjG6iGpMg-1771474751-1.2.1.1-ukZ85vKFVvLmOr_Y99eSLuQzJiWyKgQWDu6ZtuGuKgDWuG91B4DetiDGT9UnJ8N_IH0c2KxJWawYmA5W6eAj6qlYOm8gEN4MD_XKs0e5k8BnSnLZH9e78EF_A0MT8HwghLFm_BoQpqpYIUmndEpgoO7AzmBOj1VZ_qmNzc29EGNNYT7XvrZfzqowGA0svqQcuX213cxkDwd8akVvrTMalxM8gyv3XgCGtzGGs884xvc; .thumbcache_211a882976e013454a0403b9c1967076=nHpc4iLE5MaxSYqixJP5lI/CjZiDeVmCV/g6fJaIMBrgTXoSeJjKfIvPyx5jyyzQ7OuUL6S6FJq/kPhQhiBe2w%3D%3D",
    "Referer": "https://www.kalodata.com/product"
  },
  "body": "{\"country\":\"ID\",\"startDate\":\"2026-01-20\",\"endDate\":\"2026-02-18\",\"cateIds\":[\"601152\"],\"showCateIds\":[\"601152\"],\"pageNo\":2,\"pageSize\":50,\"sort\":[{\"field\":\"revenue\",\"type\":\"DESC\"}],\"product.filter.sales_channel\":[\"VIDEO\"],\"product.filter.strategy\":\"INDEPENDENT\",\"product.filter.unit_price\":\">20000\",\"product.filter.affiliate_type\":\"PUBLIC_PLAN\",\"product.filter.creator\":\"10-100\"}",
  "method": "POST"
});
```

### RESPONSE :
```
{"success":true,"data":17966,"message":null,"cached":null,"code":null}
```