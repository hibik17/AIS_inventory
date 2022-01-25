import { memo, VFC } from "react";
import { useHistory } from "react-router";

type styleProps = {
  recommendStyle: string;
};

export const RecommendButton: VFC<styleProps> = memo((props) => {
  const { recommendStyle } = props;
  const history = useHistory();
  const RecommendPath = () => {
    history.push("/recommend");
  };

  return (
    // headerを使う際に呼び出すrecommendのボタンの作成
    <button
      onClick={RecommendPath}
      className={`text-2xl text-bold pr-8 hover:text-3xl ${recommendStyle}`}
    >
      Recommend
    </button>
  );
});
