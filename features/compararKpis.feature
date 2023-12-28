Feature: CompararKpis

  @otp15
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el otp 15 de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023-01-05_2023-01-15.csv  | 2023-01-05   | 2023-01-15 |
    |results/2023-05-01_2023-05-02.csv  | 2023-05-01   | 2023-05-02 |
    |results/2023-09-01_2023-09-30.csv  | 2023-09-01   | 2023-09-30 |

  @otp15wxcta
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el otp 15 wx & cta de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023-01-05_2023-01-15.csv  | 2023-01-05   | 2023-01-15 |
    |results/2023-05-01_2023-05-02.csv  | 2023-05-01   | 2023-05-02 |
    |results/2023-09-01_2023-09-30.csv  | 2023-09-01   | 2023-09-30 |

  @btp0
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el btp 0 de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023-01-05_2023-01-15.csv  | 2023-01-05   | 2023-01-15 |
    |results/2023-05-01_2023-05-02.csv  | 2023-05-01   | 2023-05-02 |
    |results/2023-09-01_2023-09-30.csv  | 2023-09-01   | 2023-09-30 |

  @btp5
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el btp 5 de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023-01-05_2023-01-15.csv  | 2023-01-05   | 2023-01-15 |
    |results/2023-05-01_2023-05-02.csv  | 2023-05-01   | 2023-05-02 |
    |results/2023-09-01_2023-09-30.csv  | 2023-09-01   | 2023-09-30 |

  @atd0
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el atd 0 de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023-01-05_2023-01-15.csv  | 2023-01-05   | 2023-01-15 |
    |results/2023-05-01_2023-05-02.csv  | 2023-05-01   | 2023-05-02 |
    |results/2023-09-01_2023-09-30.csv  | 2023-09-01   | 2023-09-30 |

  @atd5
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el atd 5 de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023_0101_0331_all.csv     | 2023-01-01   | 2023-03-31 |

  @gtp0
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el gtp 0 de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023_0101_0331_all.csv     | 2023-01-01   | 2023-03-31 |

  @gtp5
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el gtp 5 de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023_0101_0331_all.csv     | 2023-01-01   | 2023-03-31 |

  @pax
  Scenario Outline: Comparar los kpis de la clase con un csv
    Given Abriendo el csv "<filename>" con los kpis correctos
    When Se obtengan los kpis de la clase para el periodo entre "<fecha_inicio>" y "<fecha_fin>"
    Then Se comparan el pax de la clase con los del csv

    Examples:
    | filename                          | fecha_inicio | fecha_fin  |
    |results/2023_0101_0331_all.csv     | 2023-01-01   | 2023-03-31 |