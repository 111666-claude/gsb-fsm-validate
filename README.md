# fsm-validate

读一张状态机转移表（CSV：`from,event,to`），输出校验表。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m fsmcheck check --file fsm.csv
python3 -m fsmcheck --sample=reach|dead|nondet|dup|work
```

## 口径

- **起点**：始态固定叫 `start`，终态集合是 `done`。
- **可达**：沿转移从 `start` 能走到的状态都算可达，要一直走到走不动为止。
- **死状态**：可达、不在终态集合里、且没有任何出边的状态。
- **不确定**：同一状态同一事件出现多条转移。
- **重复行**：完全相同的转移行只算一条。

## 不变量

- `start` 永远可达。
- 死状态一定可达，且不含终态。
- 不确定转移的键一定在同一状态同一事件上出现多次。
- `scanned` 不随转移条数平方级放大：两千条转移的 `scanned` 不超过 9000。

## 输出契约

`check` 打印对齐表格，列顺序为 `state`、`reachable`、`dead`、`nondet`，末行 `transitions=N`。
`--sample=work` 只打印 `{"rows": N, "scanned": N}`。
