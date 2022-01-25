import { memo, VFC } from "react";
import { useHistory } from "react-router";

type styleProps = {
  infoStyle: string;
};

export const InfoButton: VFC<styleProps> = memo((props) => {
  const { infoStyle } = props;

  const history = useHistory();
  const InfoPath = () => {
    history.push("/");
  };

  return (
    // headerのitemの一つであるINFOボタンの作成
    <button onClick={InfoPath} className={`text-2xl text-bold ${infoStyle}`}>
      INFO
    </button>
  );
});
